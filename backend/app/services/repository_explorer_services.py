from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.project_file import ProjectFile


class RepositoryExplorerService:

    @staticmethod
    def get_repository_files(
        db: Session,
        repository_id,
    ):

        repository = (
            db.query(Repository)
            .filter(Repository.id == repository_id)
            .first()
        )

        if repository is None:
            return None

        files = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.repository_id == repository_id
            )
            .order_by(ProjectFile.path.asc())
            .all()
        )

        return {
            "repository": repository,
            "files": files,
        }

    @staticmethod
    def get_repository_tree(
        db: Session,
        repository_id,
    ):
        repository = (
            db.query(Repository)
            .filter(Repository.id == repository_id)
            .first()
        )

        if repository is None:
            return None

        files = (
            db.query(ProjectFile)
            .filter(ProjectFile.repository_id == repository_id)
            .order_by(ProjectFile.path.asc())
            .all()
        )

        tree = {}

        for file in files:
            normalized_path = file.path.replace("\\", "/")

            parts = [
                part
                for part in normalized_path.split("/")
                if part
            ]

            current = tree

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}

                current = current[part]

            if parts:
                current[parts[-1]] = {
                    "type": "file",
                    "id": str(file.id),
                    "filename": file.filename,
                    "language": file.language,
                    "extension": file.extension,
                    "size": file.size,
                }

        return {
            "repository": repository,
            "tree": tree,
        }
        