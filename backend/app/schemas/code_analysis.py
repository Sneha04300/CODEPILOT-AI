from typing import Optional

from pydantic import BaseModel, Field


class AnalysisFindingResponse(BaseModel):
    category: str
    severity: str
    title: str
    description: str
    recommendation: Optional[str] = None
    line_number: Optional[int] = None


class CodeAnalysisResponse(BaseModel):
    success: bool

    analysis_id: str

    repository_id: str

    status: str

    total_files: int

    total_findings: int

    findings: list[AnalysisFindingResponse]


class AnalysisOptionsRequest(BaseModel):
    include_security: bool = True
    include_bugs: bool = True
    include_quality: bool = True
    include_performance: bool = True

    max_files: int = Field(
        default=20,
        ge=1,
        le=100,
    )