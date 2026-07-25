import uuid

from pydantic import BaseModel, Field


class AIQuestionRequest(BaseModel):

    repository_id: uuid.UUID

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

class CodeExplainRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
    )

    language: str = "Unknown"
    filename: str = "Unknown"

class RepositoryFileExplainRequest(BaseModel):
    repository_id: uuid.UUID
    file_id: uuid.UUID