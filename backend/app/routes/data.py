import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

# parents[2] = backend/
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "sample_data.json"


@router.get("/data")
def get_markers():
    """Return all markers; returns empty list on fresh deploy before any uploads."""
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text())
