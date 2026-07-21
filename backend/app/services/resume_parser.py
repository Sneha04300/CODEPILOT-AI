from app.schemas.resume import ResumeData, ResumeResponse
from app.services.pdf_extractor import PDFExtractor
from app.services.groq_parser import GroqParser
from app.services.regex_parser import RegexParser


class ResumeParserService:

    @staticmethod
    def validate_groq_output(data: dict) -> ResumeData | None:
        try:
            return ResumeData(**data)
        except Exception:
            return None

    @staticmethod
    def parse(file_path: str) -> ResumeResponse:
        text = PDFExtractor.extract_text(file_path)

        if not text.strip():
            return ResumeResponse(
                success=False,
                source="none",
                message="Could not extract text from PDF.",
            )

        groq_data = GroqParser.parse_resume(text)

        if groq_data is not None:
            validated = ResumeParserService.validate_groq_output(groq_data)
            if validated is not None:
                return ResumeResponse(
                    success=True,
                    data=validated,
                    source="groq",
                )

        fallback = RegexParser.parse_resume(text)

        return ResumeResponse(
            success=True,
            data=fallback,
            source="regex",
            message="AI parsing failed; used regex fallback."
            if groq_data is not None
            else "Groq API not configured; used regex parser.",
        )
