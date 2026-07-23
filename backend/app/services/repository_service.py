import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate


class RepositoryService:

    @staticmethod
    def create_repository(
        db: Session,
        data: RepositoryCreate,
        user_id: uuid.UUID,
        project_path: str,
        total_files: int = 0,
    ):

        repository = Repository(
            user_id=user_id,
            name=data.name,
            description=data.description,
            language=data.language or "Unknown",
            source=data.source,
            status="Indexing",
            progress=0,
            total_files=total_files,
            github_url=None,
            project_path=project_path,
        )

        db.add(repository)
        db.commit()
        db.refresh(repository)

        return repository