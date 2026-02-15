import sys
import os

# Add the backend directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from routers import graphs, algorithms, presets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Graph Theory Visualizer",
    description="An interactive web app for visualizing graph theory algorithms",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphs.router)
app.include_router(algorithms.router)
app.include_router(presets.router)


# Serve the Vue frontend in production
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    from fastapi.responses import FileResponse

    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
