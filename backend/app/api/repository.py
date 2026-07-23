import uuid

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.repository import RepositoryCreate

from app.services.repository_service import RepositoryService
from app.services.zip_service import ZipService

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

        user_id = uuid.UUID(
            "66a17f8d-df17-48cb-a870-106509ec5f96"
        )

        zip_path = save_uploaded_zip(file)

        project_folder = create_project_folder(name)

        ZipService.extract_zip(
            zip_path,
            project_folder,
        )

        total_files = ZipService.count_files(
            project_folder
        )

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

        return {
            "success": True,
            "repository": repository,
            "message": "Repository uploaded successfully.",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )