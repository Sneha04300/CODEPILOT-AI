import uuid

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.repository import RepositoryCreate
from app.services.repository_service import RepositoryService
from app.services.zip_service import ZipService
from app.services.index_service import FileIndexer
from app.services.project_file_service import ProjectFileService

from app.utils.file_utils import (
    save_uploaded_zip,
    create_project_folder,
)

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post("/upload")
def upload_repository(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(""),
    language: str = Form("Unknown"),
    db: Session = Depends(get_db),
):

    try:

        # Temporary user
        user_id = uuid.UUID(
            "66a17f8d-df17-48cb-a870-106509ec5f96"
        )

        # Save ZIP
        zip_path = save_uploaded_zip(file)

        # Create project folder
        project_folder = create_project_folder(name)

        # Extract ZIP
        ZipService.extract_zip(
            zip_path,
            project_folder,
        )

        # Count files
        total_files = ZipService.count_files(
            project_folder
        )

        # Create repository
        repository = RepositoryService.create_repository(
            db=db,
            data=RepositoryCreate(
                name=name,
                description=description,
                language=language,
                source="ZIP",
            ),
            user_id=user_id,
            project_path=project_folder,
            total_files=total_files,
        )

        # Index every source file
        files = FileIndexer.get_all_files(project_folder)

        for source_file in files:
            ProjectFileService.create_file(
                db=db,
                repository_id=repository.id,
                file_path=source_file,
                project_root=project_folder,
            )

        # Save all project files
        db.commit()

        return {
            "success": True,
            "repository": repository,
            "indexed_files": len(files),
            "message": "Repository uploaded and indexed successfully.",
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/")
def get_all_repositories(
    db: Session = Depends(get_db),
):

    repositories = RepositoryService.get_all_repositories(db)

    return {
        "success": True,
        "count": len(repositories),
        "repositories": repositories,
    }


@router.get("/{repository_id}")
def get_repository(
    repository_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    repository = RepositoryService.get_repository_by_id(
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