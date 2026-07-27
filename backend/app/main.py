from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base

# IMPORT EVERY MODEL
from app.models.user import User
from app.models.repository import Repository
from app.models.project_file import ProjectFile

from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.repository import router as repository_router
from app.api.dashboard import router as dashboard_router
from app.api.repository_explorer import router as repository_explorer_router
from app.api.ai_workspace import router as ai_workspace_router

from app.api.code_analysis import router as code_analysis_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CodePilot AI API",
    version="1.0.0"
)

# Register router AFTER app is created
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(repository_router)
app.include_router(dashboard_router)
app.include_router(repository_explorer_router)
app.include_router(ai_workspace_router)
app.include_router(code_analysis_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CodePilot AI"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }