import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
):

    summary = DashboardService.get_summary(db)

    return {
        "success": True,
        "data": summary,
    }


@router.get("/repositories")
def get_dashboard_repositories(
    db: Session = Depends(get_db),
):

    repositories = DashboardService.get_repositories(db)

    return {
        "success": True,
        "count": len(repositories),
        "repositories": [
            {
                "id": str(repo.id),
                "name": repo.name,
                "language": repo.language,
                "source": repo.source,
                "status": repo.status,
                "total_files": repo.total_files,
                "created_at": repo.created_at,
                "last_updated": repo.last_updated,
            }
            for repo in repositories
        ],
    }


@router.get("/repositories/{repository_id}")
def get_repository_details(
    repository_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    repository = DashboardService.get_repository_details(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return {
        "success": True,
        "repository": repository,
    }


@router.get("/search")
def search_repositories(
    q: str = Query(...),
    db: Session = Depends(get_db),
):

    repositories = DashboardService.search_repositories(
        db,
        q,
    )

    return {
        "success": True,
        "count": len(repositories),
        "repositories": [
            {
                "id": str(repo.id),
                "name": repo.name,
                "language": repo.language,
                "source": repo.source,
                "status": repo.status,
                "total_files": repo.total_files,
            }
            for repo in repositories
        ],
    }
@router.get("/languages")
def get_language_statistics(
    db: Session = Depends(get_db),
):

    languages = DashboardService.get_language_statistics(db)

    return {
        "success": True,
        "languages": [
            {
                "language": language,
                "count": count,
            }
            for language, count in languages
        ],
    }