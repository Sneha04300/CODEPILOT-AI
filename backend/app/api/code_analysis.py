import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.code_analysis import (
    AnalysisOptionsRequest,
)
from app.services.code_analysis_service import (
    CodeAnalysisService,
)


router = APIRouter(
    prefix="/code-analysis",
    tags=["Code Analysis"],
)


# ---------------------------------------------------------
# 1. START REPOSITORY ANALYSIS
# ---------------------------------------------------------

@router.post(
    "/repositories/{repository_id}/analyze"
)
def analyze_repository(
    repository_id: uuid.UUID,
    options: AnalysisOptionsRequest,
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # Check repository exists
    # -----------------------------------------------------

    repository = CodeAnalysisService.get_repository(
        db=db,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    # -----------------------------------------------------
    # Load repository files
    # -----------------------------------------------------

    files = CodeAnalysisService.get_repository_files(
        db=db,
        repository_id=repository_id,
        max_files=options.max_files,
    )

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Repository has no indexed files",
        )

    # -----------------------------------------------------
    # Create analysis
    # -----------------------------------------------------

    analysis = CodeAnalysisService.create_analysis(
        db=db,
        repository_id=repository_id,
        total_files=len(files),
    )

    try:
        # -------------------------------------------------
        # Mark analysis as running
        # -------------------------------------------------

        analysis = CodeAnalysisService.mark_running(
            db=db,
            analysis=analysis,
        )

        # -------------------------------------------------
        # AI analysis will be added in the next step.
        #
        # For now we only test the analysis lifecycle.
        # -------------------------------------------------

        findings = []

        # -------------------------------------------------
        # Complete analysis
        # -------------------------------------------------

        analysis = CodeAnalysisService.mark_completed(
            db=db,
            analysis=analysis,
            total_findings=len(findings),
        )

    except Exception as error:
        CodeAnalysisService.mark_failed(
            db=db,
            analysis=analysis,
        )

        raise HTTPException(
            status_code=500,
            detail="Code analysis failed",
        ) from error

    # -----------------------------------------------------
    # Return analysis result
    # -----------------------------------------------------

    return {
        "success": True,

        "repository": {
            "id": str(repository.id),
            "name": repository.name,
        },

        "analysis": {
            "id": str(analysis.id),
            "status": analysis.status,
            "total_files": analysis.total_files,
            "total_findings": (
                analysis.total_findings
            ),
            "created_at": analysis.created_at,
            "completed_at": analysis.completed_at,
        },

        "options": {
            "include_security": (
                options.include_security
            ),
            "include_bugs": (
                options.include_bugs
            ),
            "include_quality": (
                options.include_quality
            ),
            "include_performance": (
                options.include_performance
            ),
            "max_files": options.max_files,
        },

        "findings": [],
    }