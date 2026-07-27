import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.code_analysis import AnalysisOptionsRequest
from app.services.code_analysis_service import CodeAnalysisService
from app.services.static_analysis_service import StaticAnalysisService


router = APIRouter(
    prefix="/code-analysis",
    tags=["Code Analysis"],
)


# ---------------------------------------------------------
# 1. START REPOSITORY ANALYSIS
# ---------------------------------------------------------

@router.post("/repositories/{repository_id}/analyze")
def analyze_repository(
    repository_id: uuid.UUID,
    options: AnalysisOptionsRequest,
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # 1. Check repository exists
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
    # 2. Load repository files
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
    # 3. Create analysis record
    # -----------------------------------------------------

    analysis = CodeAnalysisService.create_analysis(
        db=db,
        repository_id=repository_id,
        total_files=len(files),
    )

    try:
        # -------------------------------------------------
        # 4. Mark analysis as running
        # -------------------------------------------------

        analysis = CodeAnalysisService.mark_running(
            db=db,
            analysis=analysis,
        )

        # -------------------------------------------------
        # 5. Run static analysis
        # -------------------------------------------------

        findings = []

        for file in files:
            file_findings = StaticAnalysisService.analyze_file(
                file
            )

            for finding_data in file_findings:
                category = finding_data["category"]

                # -----------------------------------------
                # Respect requested analysis options
                # -----------------------------------------

                if (
                    category == "security"
                    and not options.include_security
                ):
                    continue

                if (
                    category == "bug"
                    and not options.include_bugs
                ):
                    continue

                if (
                    category == "quality"
                    and not options.include_quality
                ):
                    continue

                if (
                    category == "performance"
                    and not options.include_performance
                ):
                    continue

                # -----------------------------------------
                # Save finding in PostgreSQL
                # -----------------------------------------

                finding = CodeAnalysisService.add_finding(
                    db=db,
                    analysis_id=analysis.id,
                    file_id=finding_data["file_id"],
                    category=finding_data["category"],
                    severity=finding_data["severity"],
                    title=finding_data["title"],
                    description=finding_data["description"],
                    recommendation=finding_data.get(
                        "recommendation"
                    ),
                    line_number=finding_data.get(
                        "line_number"
                    ),
                )

                findings.append(finding)

        # -------------------------------------------------
        # 6. Mark analysis as completed
        # -------------------------------------------------

        analysis = CodeAnalysisService.mark_completed(
            db=db,
            analysis=analysis,
            total_findings=len(findings),
        )

    except Exception as error:
        # -------------------------------------------------
        # 7. Mark analysis as failed
        # -------------------------------------------------

        CodeAnalysisService.mark_failed(
            db=db,
            analysis=analysis,
        )

        raise HTTPException(
            status_code=500,
            detail="Code analysis failed",
        ) from error

    # -----------------------------------------------------
    # 8. Return analysis report
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
            "total_findings": analysis.total_findings,
            "created_at": analysis.created_at,
            "completed_at": analysis.completed_at,
        },

        "options": {
            "include_security": options.include_security,
            "include_bugs": options.include_bugs,
            "include_quality": options.include_quality,
            "include_performance": options.include_performance,
            "max_files": options.max_files,
        },

        "findings": [
            {
                "id": str(finding.id),

                "file_id": (
                    str(finding.file_id)
                    if finding.file_id
                    else None
                ),

                "category": finding.category,
                "severity": finding.severity,
                "title": finding.title,
                "description": finding.description,
                "recommendation": finding.recommendation,
                "line_number": finding.line_number,
            }
            for finding in findings
        ],
    }

    

# ---------------------------------------------------------
# 2. GET ANALYSIS REPORT
# ---------------------------------------------------------

@router.get("/{analysis_id}")
def get_analysis_report(
    analysis_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    analysis = CodeAnalysisService.get_analysis(
        db=db,
        analysis_id=analysis_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    findings = CodeAnalysisService.get_findings(
        db=db,
        analysis_id=analysis_id,
    )

    return {
        "success": True,

        "analysis": {
            "id": str(analysis.id),
            "repository_id": str(
                analysis.repository_id
            ),
            "status": analysis.status,
            "total_files": analysis.total_files,
            "total_findings": analysis.total_findings,
            "created_at": analysis.created_at,
            "completed_at": analysis.completed_at,
        },

        "findings": [
            {
                "id": str(finding.id),
                "file_id": (
                    str(finding.file_id)
                    if finding.file_id
                    else None
                ),
                "category": finding.category,
                "severity": finding.severity,
                "title": finding.title,
                "description": finding.description,
                "recommendation": finding.recommendation,
                "line_number": finding.line_number,
                "created_at": finding.created_at,
            }
            for finding in findings
        ],
    }

# ---------------------------------------------------------
# 3. GET REPOSITORY ANALYSIS HISTORY
# ---------------------------------------------------------

@router.get(
    "/repositories/{repository_id}/analyses"
)
def get_repository_analysis_history(
    repository_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    repository = CodeAnalysisService.get_repository(
        db=db,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    analyses = CodeAnalysisService.get_repository_analyses(
        db=db,
        repository_id=repository_id,
    )

    return {
        "success": True,
        "repository": {
            "id": str(repository.id),
            "name": repository.name,
        },
        "count": len(analyses),
        "analyses": [
            {
                "id": str(analysis.id),
                "status": analysis.status,
                "total_files": analysis.total_files,
                "total_findings": analysis.total_findings,
                "created_at": analysis.created_at,
                "completed_at": analysis.completed_at,
            }
            for analysis in analyses
        ],
    }