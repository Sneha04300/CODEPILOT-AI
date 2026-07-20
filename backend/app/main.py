from fastapi import FastAPI

from app.db.database import engine, Base
from app.db import base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CodePilot AI API",
    version="1.0.0",
    description="Backend API for CodePilot AI"
)

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Welcome to CodePilot AI Backend 🚀"
    }

@app.get("/health")
async def health():
    return {
        "status": "Healthy"
    }