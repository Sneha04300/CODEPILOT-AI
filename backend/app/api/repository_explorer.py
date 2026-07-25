import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.repository_explorer_services import RepositoryExplorerService


router = APIRouter(
    prefix="/explorer",
    tags=["Repository Explorer"],
)


@router.get("/{repository_id}/files")
def get_repository_files(
    repository_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    result = RepositoryExplorerService.get_repository_files(
        db=db,
        repository_id=repository_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    repository = result["repository"]
    files = result["files"]

    return {
        "success": True,
        "repository": {
            "id": str(repository.id),
            "name": repository.name,
            "language": repository.language,
            "source": repository.source,
        },
        "total_files": len(files),
        "files": [
            {
                "id": str(file.id),
                "filename": file.filename,
                "path": file.path,
                "extension": file.extension,
                "language": file.language,
                "tokens": file.tokens,
                "size": file.size,
            }
            for file in files
        ],
    }
@router.get("/{repository_id}/tree")
def get_repository_tree(
    repository_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    result = RepositoryExplorerService.get_repository_tree(
        db=db,
        repository_id=repository_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    repository = result["repository"]

    return {
        "success": True,
        "repository": {
            "id": str(repository.id),
            "name": repository.name,
        },
        "tree": result["tree"],
    }

@router.get("/{repository_id}/files/{file_id}")
def get_file_content(
    repository_id: uuid.UUID,
    file_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    file = RepositoryExplorerService.get_file_content(
        db=db,
        repository_id=repository_id,
        file_id=file_id,
    )

    if file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    return {
        "success": True,
        "file": {
            "id": str(file.id),
            "repository_id": str(file.repository_id),
            "filename": file.filename,
            "path": file.path,
            "extension": file.extension,
            "language": file.language,
            "tokens": file.tokens,
            "size": file.size,
            "content": file.content,
        },
    }