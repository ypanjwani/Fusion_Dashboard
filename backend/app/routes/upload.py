from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import parser, storage

router = APIRouter()

ALLOWED_EXTENSIONS = {"csv", "json", "xlsx", "jpg", "jpeg"}


def _ext(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = _ext(file.filename)

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # Read once — reused for both saving and parsing
    contents = await file.read()
    file_url = storage.save_file(file.filename, contents)

    if ext == "csv":
        markers = parser.parse_csv(contents)
        saved   = storage.append_markers(markers)
        return {"status": "ok", "type": "csv", "markers_parsed": len(saved), "markers": saved}

    if ext == "xlsx":
        markers = parser.parse_xlsx(contents)
        saved   = storage.append_markers(markers)
        return {"status": "ok", "type": "xlsx", "markers_parsed": len(saved), "markers": saved}

    if ext == "json":
        markers = parser.parse_json(contents)
        saved   = storage.append_markers(markers)
        return {"status": "ok", "type": "json", "markers_parsed": len(saved), "markers": saved}

    # Image — return the URL so the frontend can attach it to a marker
    return {"status": "ok", "type": "image", "file_url": file_url}
