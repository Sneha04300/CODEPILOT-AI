from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


# -----------------------------
# Used while uploading repository
# -----------------------------
class RepositoryCreate(BaseModel):
    name: str
    description: str = ""
    language: str = "Unknown"
    source: str


# -----------------------------
# Returned from API
# -----------------------------
class RepositoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None = None
    language: str
    source: str
    status: str
    progress: int
    total_files: int
    github_url: str | None = None
    project_path: str
    created_at: datetime

    class Config:
        from_attributes = True