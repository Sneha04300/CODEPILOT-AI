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

    @staticmethod
    def get_language_statistics(db):

        languages = (
            db.query(
                Repository.language,
                func.count(Repository.id).label("count")
            )
            .group_by(Repository.language)
            .order_by(func.count(Repository.id).desc())
            .all()
        )

        return languages

    @staticmethod
    def get_recent_repositories(db, limit: int = 5):

        repositories = (
            db.query(Repository)
            .order_by(Repository.created_at.desc())
            .limit(limit)
            .all()
        )

        return repositories

    @staticmethod
    def get_github_repositories(db):

        repositories = (
            db.query(Repository)
            .filter(
                Repository.source == "GitHub"
            )
            .order_by(
                Repository.created_at.desc()
            )
            .all()
        )

        return repositories

    @staticmethod
    def get_dashboard_statistics(db):

        total_repositories = (
            db.query(func.count(Repository.id))
            .scalar()
            or 0
        )

        total_files = (
            db.query(func.count(ProjectFile.id))
            .scalar()
            or 0
        )

        total_size = (
            db.query(func.sum(ProjectFile.size))
            .scalar()
            or 0
        )

        total_languages = (
            db.query(ProjectFile.language)
            .distinct()
            .count()
        )

        github_repositories = (
            db.query(func.count(Repository.id))
            .filter(Repository.source == "GitHub")
            .scalar()
            or 0
        )

        recent_repositories = (
            db.query(func.count(Repository.id))
            .filter(Repository.created_at.isnot(None))
            .scalar()
            or 0
        )

        return {
            "total_repositories": total_repositories,
            "total_files": total_files,
            "total_size": total_size,
            "total_languages": total_languages,
            "github_repositories": github_repositories,
            "recent_repositories": recent_repositories,
        }