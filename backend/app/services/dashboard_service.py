from sqlalchemy import func, or_

from app.models.repository import Repository
from app.models.project_file import ProjectFile


class DashboardService:

    @staticmethod
    def get_summary(db):

        repositories = db.query(func.count(Repository.id)).scalar() or 0

        files = db.query(func.count(ProjectFile.id)).scalar() or 0

        total_size = db.query(func.sum(ProjectFile.size)).scalar() or 0

        languages = (
            db.query(ProjectFile.language)
            .distinct()
            .count()
        )

        return {
            "total_repositories": repositories,
            "total_files": files,
            "total_size": total_size,
            "total_languages": languages,
        }

    @staticmethod
    def get_repositories(db):

        repositories = (
            db.query(Repository)
            .order_by(Repository.created_at.desc())
            .all()
        )

        return repositories

    @staticmethod
    def get_repository_details(
        db,
        repository_id,
    ):

        repository = (
            db.query(Repository)
            .filter_by(id=repository_id)
            .first()
        )

        return repository

    @staticmethod
    def search_repositories(
        db,
        query: str,
    ):

        repositories = (
            db.query(Repository)
            .filter(
                or_(
                    Repository.name.ilike(f"%{query}%"),
                    Repository.description.ilike(f"%{query}%"),
                    Repository.language.ilike(f"%{query}%"),
                )
            )
            .order_by(Repository.created_at.desc())
            .all()
        )

        return repositories