from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.project_file import ProjectFile
from app.models.code_analysis import CodeAnalysis
from app.models.analysis_finding import AnalysisFinding


class CodeAnalysisService:

    # ---------------------------------------------------------
    # 1. GET REPOSITORY
    # ---------------------------------------------------------

    @staticmethod
    def get_repository(
        db: Session,
        repository_id,
    ):
        return (
            db.query(Repository)
            .filter(
                Repository.id == repository_id
            )
            .first()
        )

    # ---------------------------------------------------------
    # 2. GET FILES TO ANALYZE
    # ---------------------------------------------------------

    @staticmethod
    def get_repository_files(
        db: Session,
        repository_id,
        max_files: int = 20,
    ):
        files = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.repository_id == repository_id
            )
            .order_by(
                ProjectFile.path.asc()
            )
            .limit(max_files)
            .all()
        )

        return files

    # ---------------------------------------------------------
    # 3. CREATE ANALYSIS
    # ---------------------------------------------------------

    @staticmethod
    def create_analysis(
        db: Session,
        repository_id,
        total_files: int,
    ):
        analysis = CodeAnalysis(
            repository_id=repository_id,
            status="pending",
            total_files=total_files,
            total_findings=0,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    # ---------------------------------------------------------
    # 4. MARK ANALYSIS AS RUNNING
    # ---------------------------------------------------------

    @staticmethod
    def mark_running(
        db: Session,
        analysis: CodeAnalysis,
    ):
        analysis.status = "running"

        db.commit()
        db.refresh(analysis)

        return analysis

    # ---------------------------------------------------------
    # 5. ADD FINDING
    # ---------------------------------------------------------

    @staticmethod
    def add_finding(
        db: Session,
        analysis_id,
        category: str,
        severity: str,
        title: str,
        description: str,
        recommendation: str | None = None,
        line_number: int | None = None,
        file_id=None,
    ):
        finding = AnalysisFinding(
            analysis_id=analysis_id,
            file_id=file_id,
            category=category,
            severity=severity,
            title=title,
            description=description,
            recommendation=recommendation,
            line_number=line_number,
        )

        db.add(finding)
        db.commit()
        db.refresh(finding)

        return finding

    # ---------------------------------------------------------
    # 6. MARK ANALYSIS AS COMPLETED
    # ---------------------------------------------------------

    @staticmethod
    def mark_completed(
        db: Session,
        analysis: CodeAnalysis,
        total_findings: int,
    ):
        analysis.status = "completed"
        analysis.total_findings = total_findings
        analysis.completed_at = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(analysis)

        return analysis

    # ---------------------------------------------------------
    # 7. MARK ANALYSIS AS FAILED
    # ---------------------------------------------------------

    @staticmethod
    def mark_failed(
        db: Session,
        analysis: CodeAnalysis,
    ):
        analysis.status = "failed"
        analysis.completed_at = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(analysis)

        return analysis

    # ---------------------------------------------------------
    # 8. GET ANALYSIS
    # ---------------------------------------------------------

    @staticmethod
    def get_analysis(
        db: Session,
        analysis_id,
    ):
        return (
            db.query(CodeAnalysis)
            .filter(
                CodeAnalysis.id == analysis_id
            )
            .first()
        )

    # ---------------------------------------------------------
    # 9. GET FINDINGS
    # ---------------------------------------------------------

    @staticmethod
    def get_findings(
        db: Session,
        analysis_id,
    ):
        return (
            db.query(AnalysisFinding)
            .filter(
                AnalysisFinding.analysis_id
                == analysis_id
            )
            .order_by(
                AnalysisFinding.created_at.asc()
            )
            .all()
        )