import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

# parents[2] = backend/
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "sample_data.json"


@router.get("/data")
def get_markers():
    """Return all markers from sample_data.json."""
    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail="sample_data.json not found")
    return json.loads(DATA_FILE.read_text())
