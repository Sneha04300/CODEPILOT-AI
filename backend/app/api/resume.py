import tempfile
import os

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_parser import ResumeParserService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        content = await file.read()
        tmp.write(content)
        tmp.close()

        result = ResumeParserService.parse(tmp.name)

        if not result.success:
            raise HTTPException(
                status_code=422,
                detail=result.message or "Failed to parse resume.",
            )

        return result

    finally:
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)
