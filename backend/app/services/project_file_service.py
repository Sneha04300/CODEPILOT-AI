import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.project_file import ProjectFile


class ProjectFileService:

    @staticmethod
    def create_file(
        db: Session,
        repository_id: uuid.UUID,
        file_path: Path,
        project_root: str,
    ):

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            content = ""

        relative_path = str(
            file_path.relative_to(project_root)
        )

        project_file = ProjectFile(
            repository_id=repository_id,
            filename=file_path.name,
            path=relative_path,
            extension=file_path.suffix,
            language=file_path.suffix.replace(".", ""),
            content=content,
            tokens=len(content.split()),
            size=len(content),
        )

        db.add(project_file)