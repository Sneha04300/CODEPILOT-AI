from pathlib import Path


class FileIndexer:

    ALLOWED_EXTENSIONS = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".go",
        ".php",
        ".html",
        ".css",
        ".scss",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".md",
        ".txt",
        ".sql",
        ".sh",
    }

    @staticmethod
    def get_all_files(project_path: str):

        project = Path(project_path)

        files = []

        for file in project.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() not in FileIndexer.ALLOWED_EXTENSIONS:
                continue

            files.append(file)

        return files

    @staticmethod
    def read_file(file_path: Path):

        try:
            return file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except Exception:
            return ""