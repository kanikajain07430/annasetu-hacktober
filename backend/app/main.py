import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.session import init_db
from app.api.router import api_router

# Configure UTF-8 for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Smart Agricultural Procurement & Surplus Redistribution Platform Backend Service",
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize and seed database
@app.on_event("startup")
def on_startup():
    init_db()
    print(">> AnnaSetu Database initialized and seeded successfully.")

# Mount API V1 Router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Health Check
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "AnnaSetu AgTech & Redistribution Platform",
        "version": settings.PROJECT_VERSION,
        "operational": True
    }

# Mount Frontend static directories
FRONTEND_DIR = os.path.join(os.path.dirname(settings.BASE_DIR), "frontend")
if not os.path.exists(FRONTEND_DIR):
    FRONTEND_DIR = os.path.join(settings.BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    css_dir = os.path.join(FRONTEND_DIR, "css")
    js_dir = os.path.join(FRONTEND_DIR, "js")
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")

@app.get("/", response_class=HTMLResponse, tags=["Frontend App"])
def serve_frontend_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>AnnaSetu API Running. Visit <a href='/docs'>/docs</a></h1>")
