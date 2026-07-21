from pypdf import PdfReader


class PDFExtractor:

    @staticmethod
    def extract_text(file_path: str) -> str:
        reader = PdfReader(file_path)
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts)
