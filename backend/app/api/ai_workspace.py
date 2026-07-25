from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.ai_workspcae import (
    AIQuestionRequest,
    CodeExplainRequest,
    RepositoryFileExplainRequest,
)

from app.services.ai_workspace_service import AIWorkspaceService
from app.services.ai_service import AIService


router = APIRouter(
    prefix="/ai-workspace",
    tags=["AI Workspace"],
)


# ---------------------------------------------------------
# 1. ASK QUESTIONS ABOUT A REPOSITORY
# ---------------------------------------------------------

@router.post("/ask")
def ask_repository_question(
    data: AIQuestionRequest,
    db: Session = Depends(get_db),
):

    # Load repository and indexed files
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

    # Find files relevant to the user's question
    relevant_files = AIWorkspaceService.find_relevant_files(
        db=db,
        repository_id=data.repository_id,
        question=data.question,
    )

    # Build context from relevant source files
    context_result = AIWorkspaceService.build_context(
        relevant_files
    )

    # Send question + repository context to Groq
    ai_answer = AIService.ask_repository(
        question=data.question,
        context=context_result["context"],
    )

    return {
        "success": True,

        "repository": {
            "id": str(repository.id),
            "name": repository.name,
        },

        "question": data.question,

        "answer": ai_answer,

        "sources": [
            {
                "id": str(file.id),
                "filename": file.filename,
                "path": file.path,
                "language": file.language,
            }
            for file in context_result["included_files"]
        ],

        "context_info": {
            "available_files": len(files),
            "relevant_files": len(relevant_files),
            "included_files": len(
                context_result["included_files"]
            ),
            "characters": context_result["characters"],
        },
    }


# ---------------------------------------------------------
# 2. EXPLAIN MANUALLY PROVIDED CODE
# ---------------------------------------------------------

@router.post("/explain")
def explain_code(
    data: CodeExplainRequest,
):

    explanation = AIService.explain_code(
        code=data.code,
        language=data.language,
        filename=data.filename,
    )

    return {
        "success": True,
        "filename": data.filename,
        "language": data.language,
        "explanation": explanation,
    }


# ---------------------------------------------------------
# 3. EXPLAIN A FILE FROM AN INDEXED REPOSITORY
# ---------------------------------------------------------

@router.post("/explain-file")
def explain_repository_file(
    data: RepositoryFileExplainRequest,
    db: Session = Depends(get_db),
):

    # Find the requested file inside the repository
    file = AIWorkspaceService.get_repository_file(
        db=db,
        repository_id=data.repository_id,
        file_id=data.file_id,
    )

    if file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found in this repository",
        )

    # Send actual stored source code to AI
    explanation = AIService.explain_code(
        code=file.content,
        language=file.language,
        filename=file.filename,
    )

    return {
        "success": True,

        "file": {
            "id": str(file.id),
            "repository_id": str(file.repository_id),
            "filename": file.filename,
            "path": file.path,
            "language": file.language,
            "extension": file.extension,
        },

        "explanation": explanation,
    }