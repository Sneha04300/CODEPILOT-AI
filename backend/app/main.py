from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CodePilot AI API",
    version="1.0.0"
)

# Register router AFTER app is created
app.include_router(auth_router)
app.include_router(resume_router)


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