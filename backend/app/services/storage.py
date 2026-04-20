from __future__ import annotations
import json
from pathlib import Path

UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"
DATA_FILE  = Path(__file__).resolve().parents[3] / "data" / "sample_data.json"


def save_file(filename: str, contents: bytes) -> str:
    """Write raw bytes to uploads/ and return a URL-friendly relative path."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    (UPLOAD_DIR / filename).write_bytes(contents)
    return f"uploads/{filename}"


def _load_markers() -> list[dict]:
    """Read sample_data.json; return empty list on missing or corrupt file."""
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return []


def _next_id(existing: list[dict]) -> int:
    if not existing:
        return 1
    return max(m.get("id", 0) for m in existing) + 1


def append_markers(new_markers: list[dict]) -> list[dict]:
    """Stamp each marker with a unique ID, append to sample_data.json, and return stamped list."""
    existing = _load_markers()
    next_id  = _next_id(existing)
    stamped  = [{"id": next_id + i, **m} for i, m in enumerate(new_markers)]
    existing.extend(stamped)
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(existing, indent=2))
    return stamped
