from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.ai_workspcae import AIQuestionRequest
from app.services.ai_workspace_service import AIWorkspaceService


router = APIRouter(
    prefix="/ai-workspace",
    tags=["AI Workspace"],
)


@router.post("/ask")
def ask_repository_question(
    data: AIQuestionRequest,
    db: Session = Depends(get_db),
):

    # 1. Load repository and files
    result = AIWorkspaceService.get_repository_context(
        db=db,
        repository_id=data.repository_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    repository = result["repository"]
    files = result["files"]

    # 2. Find relevant files
    relevant_files = AIWorkspaceService.find_relevant_files(
        db=db,
        repository_id=data.repository_id,
        question=data.question,
    )

    # 3. Build AI context from relevant files
    context_result = AIWorkspaceService.build_context(
        relevant_files
    )

    # 4. Return test response
    return {
        "success": True,

        "repository": {
            "id": str(repository.id),
            "name": repository.name,
        },

        "question": data.question,

        "available_files": len(files),

        "relevant_files": [
            {
                "id": str(file.id),
                "filename": file.filename,
                "path": file.path,
                "language": file.language,
                "tokens": file.tokens,
            }
            for file in relevant_files
        ],

        "context": {
            "included_files": len(
                context_result["included_files"]
            ),
            "characters": context_result["characters"],
            "preview": context_result["context"][:1000],
        },

        "message": "AI context built successfully.",
    }