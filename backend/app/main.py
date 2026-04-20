from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import data, upload

app = FastAPI(title="Fusion Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)
app.include_router(upload.router)

# Base directory = backend/
BASE_DIR = Path(__file__).resolve().parents[1]

# Serve uploaded images at /uploads/<filename>
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Serve frontend static assets (css, js, assets)
app.mount("/css",    StaticFiles(directory=str(BASE_DIR / "frontend" / "css")),    name="css")
app.mount("/js",     StaticFiles(directory=str(BASE_DIR / "frontend" / "js")),     name="js")
app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "frontend" / "assets")), name="assets")


@app.get("/")
def serve_index():
    """Serve the frontend index.html."""
    return FileResponse(str(BASE_DIR / "frontend" / "index.html"))
