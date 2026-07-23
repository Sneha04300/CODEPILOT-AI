from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class RepositoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    language: Optional[str] = None
    source: str


class RepositoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str]
    language: Optional[str]
    source: str
    status: str

    class Config:
        from_attributes = True