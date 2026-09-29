from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import Base, engine
from .routes.pages import router as pages_router
from .routes.auth_routes import router as auth_router
from .routes.planners import router as planners_router
from .routes.history import router as history_router

BASE_DIR = Path(__file__).resolve().parent.parent
Path("uploads").mkdir(exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(planners_router)
app.include_router(history_router)

@app.get("/startup")
def startup():
    return {"status": "ready", "app": settings.app_name}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
