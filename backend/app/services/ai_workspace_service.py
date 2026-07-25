from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.project_file import ProjectFile


class AIWorkspaceService:

    @staticmethod
    def get_repository_context(
        db: Session,
        repository_id,
    ):

        repository = (
            db.query(Repository)
            .filter(Repository.id == repository_id)
            .first()
        )

        if repository is None:
            return None

        files = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.repository_id == repository_id
            )
            .order_by(ProjectFile.path.asc())
            .all()
        )

        return {
            "repository": repository,
            "files": files,
        }

    @staticmethod
    def find_relevant_files(
        db: Session,
        repository_id,
        question: str,
        limit: int = 10,
    ):

        words = [
            word.lower()
            for word in question.split()
            if len(word) >= 3
        ]

        files = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.repository_id == repository_id
            )
            .all()
        )

        scored_files = []

        for file in files:

            filename = (file.filename or "").lower()
            path = (file.path or "").lower()
            content = (file.content or "").lower()

            score = 0

            for word in words:

                if word in filename:
                    score += 5

                if word in path:
                    score += 3

                if word in content:
                    score += 1

            if score > 0:
                scored_files.append(
                    (score, file)
                )

        scored_files.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            file
            for score, file in scored_files[:limit]
        ]

    @staticmethod
    def build_context(
        files,
        max_characters: int = 30000,
    ):

        context_parts = []
        current_size = 0
        included_files = []

        for file in files:

            content = file.content or ""

            file_context = (
                f"\n--- FILE: {file.path} ---\n"
                f"Language: {file.language}\n\n"
                f"{content}\n"
            )

            remaining_space = max_characters - current_size

            if remaining_space <= 0:
                break

            if len(file_context) > remaining_space:
                file_context = file_context[:remaining_space]

            context_parts.append(file_context)
            included_files.append(file)

            current_size += len(file_context)

            if current_size >= max_characters:
                break

        return {
            "context": "\n".join(context_parts),
            "included_files": included_files,
            "characters": current_size,
        }