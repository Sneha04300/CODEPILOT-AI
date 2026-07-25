from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.project_file import ProjectFile

from sqlalchemy import func


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

    @staticmethod
    def get_file_content(
        db: Session,
        repository_id,
        file_id,
    ):
        file = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.id == file_id,
                ProjectFile.repository_id == repository_id,
            )
            .first()
        )

        return file

    @staticmethod
    def search_files(
        db: Session,
        repository_id,
        query: str,
    ):
        files = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.repository_id == repository_id
            )
            .filter(
                (
                    ProjectFile.filename.ilike(f"%{query}%")
                )
                |
                (
                    ProjectFile.path.ilike(f"%{query}%")
                )
                |
                (
                    ProjectFile.content.ilike(f"%{query}%")
                )
            )
            .order_by(ProjectFile.path.asc())
            .limit(100)
            .all()
        )

        return files

    @staticmethod
    def get_repository_statistics(
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

        total_files = (
            db.query(func.count(ProjectFile.id))
            .filter(ProjectFile.repository_id == repository_id)
            .scalar()
            or 0
        )

        total_size = (
            db.query(func.sum(ProjectFile.size))
            .filter(ProjectFile.repository_id == repository_id)
            .scalar()
            or 0
        )

        total_tokens = (
            db.query(func.sum(ProjectFile.tokens))
            .filter(ProjectFile.repository_id == repository_id)
            .scalar()
            or 0
        )

        languages = (
            db.query(
                ProjectFile.language,
                func.count(ProjectFile.id).label("count"),
            )
            .filter(ProjectFile.repository_id == repository_id)
            .group_by(ProjectFile.language)
            .order_by(func.count(ProjectFile.id).desc())
            .all()
        )

        return {
            "repository": repository,
            "total_files": total_files,
            "total_size": total_size,
            "total_tokens": total_tokens,
            "languages": languages,
        }
        