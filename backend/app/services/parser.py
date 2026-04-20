from __future__ import annotations
import csv
import json
import io
import openpyxl


def _build_marker(lat, lon, type_, description) -> dict:
    return {
        "lat": float(lat),
        "lon": float(lon),
        "type": str(type_).strip(),
        "description": str(description).strip(),
    }


def parse_csv(contents: bytes) -> list[dict]:
    """Parse CSV bytes into a list of marker dicts; skips rows with missing/bad lat-lon."""
    reader = csv.DictReader(io.StringIO(contents.decode("utf-8")))
    markers = []
    for row in reader:
        try:
            markers.append(_build_marker(
                row["lat"], row["lon"],
                row.get("type", "OSINT"),
                row.get("description", ""),
            ))
        except (KeyError, ValueError):
            continue
    return markers


def parse_xlsx(contents: bytes) -> list[dict]:
    """Parse Excel (.xlsx) bytes into marker dicts; first row must be headers."""
    wb = openpyxl.load_workbook(io.BytesIO(contents), read_only=True, data_only=True)
    ws = wb.active
    rows = iter(ws.rows)
    headers = [str(cell.value).strip().lower() for cell in next(rows)]
    markers = []
    for row in rows:
        data = {headers[i]: cell.value for i, cell in enumerate(row)}
        try:
            markers.append(_build_marker(
                data["lat"], data["lon"],
                data.get("type") or "OSINT",
                data.get("description") or "",
            ))
        except (KeyError, ValueError, TypeError):
            continue
    wb.close()
    return markers


def parse_json(contents: bytes) -> list[dict]:
    """Parse JSON bytes (list or {markers:[]} shape) into marker dicts."""
    data = json.loads(contents)
    if isinstance(data, dict):
        data = data.get("markers", [data])
    markers = []
    for item in data:
        try:
            markers.append(_build_marker(
                item["lat"], item["lon"],
                item.get("type", "OSINT"),
                item.get("description", ""),
            ))
        except (KeyError, ValueError):
            continue
    return markers
