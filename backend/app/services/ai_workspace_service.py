import re

from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.project_file import ProjectFile


class AIWorkspaceService:

    # ---------------------------------------------------------
    # 1. GET REPOSITORY CONTEXT
    # ---------------------------------------------------------

    @staticmethod
    def get_repository_context(
        db: Session,
        repository_id,
    ):
        repository = (
            db.query(Repository)
            .filter(
                Repository.id == repository_id
            )
            .first()
        )

        if repository is None:
            return None

        files = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.repository_id == repository_id
            )
            .order_by(
                ProjectFile.path.asc()
            )
            .all()
        )

        return {
            "repository": repository,
            "files": files,
        }


    # ---------------------------------------------------------
    # 2. FIND RELEVANT FILES
    # ---------------------------------------------------------

    @staticmethod
    def find_relevant_files(
        db: Session,
        repository_id,
        question: str,
        limit: int = 10,
    ):
        files = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.repository_id == repository_id
            )
            .all()
        )

        if not files:
            return []

        # Clean question and extract useful keywords
        words = re.findall(
            r"[a-zA-Z0-9_]+",
            question.lower(),
        )

        # Common words that don't help identify source files
        stop_words = {
            "the",
            "and",
            "for",
            "that",
            "this",
            "with",
            "from",
            "how",
            "what",
            "where",
            "when",
            "which",
            "why",
            "does",
            "are",
            "is",
            "was",
            "were",
            "can",
            "could",
            "would",
            "should",
            "into",
            "about",
            "work",
            "works",
            "working",
            "project",
            "code",
            "file",
            "files",
        }

        keywords = {
            word
            for word in words
            if len(word) >= 3
            and word not in stop_words
        }

        # -----------------------------------------------------
        # Expand common developer concepts
        # -----------------------------------------------------

        concept_keywords = {
            "auth": {
                "auth",
                "authentication",
                "login",
                "register",
                "signup",
                "signin",
                "jwt",
                "token",
                "password",
                "bcrypt",
                "session",
                "user",
                "middleware",
            },

            "authentication": {
                "auth",
                "authentication",
                "login",
                "register",
                "signup",
                "signin",
                "jwt",
                "token",
                "password",
                "bcrypt",
                "session",
                "user",
                "middleware",
            },

            "database": {
                "database",
                "db",
                "model",
                "models",
                "schema",
                "sql",
                "sqlalchemy",
                "postgres",
                "postgresql",
                "migration",
                "repository",
            },

            "api": {
                "api",
                "route",
                "routes",
                "router",
                "endpoint",
                "controller",
                "service",
                "request",
                "response",
            },

            "repository": {
                "repository",
                "repo",
                "github",
                "clone",
                "branch",
                "commit",
                "project",
            },

            "upload": {
                "upload",
                "file",
                "files",
                "multipart",
                "storage",
                "parser",
            },

            "ai": {
                "ai",
                "groq",
                "llm",
                "prompt",
                "completion",
                "chat",
                "assistant",
                "model",
            },

            "conversation": {
                "conversation",
                "message",
                "messages",
                "chat",
                "history",
                "assistant",
                "user",
            },
        }

        expanded_keywords = set(keywords)

        for keyword in keywords:
            if keyword in concept_keywords:
                expanded_keywords.update(
                    concept_keywords[keyword]
                )

        scored_files = []

        for file in files:
            filename = (
                file.filename or ""
            ).lower()

            path = (
                file.path or ""
            ).lower()

            content = (
                file.content or ""
            ).lower()

            language = (
                file.language or ""
            ).lower()

            score = 0
            matched_keywords = set()

            for keyword in expanded_keywords:

                # Filename match = strongest signal
                if keyword in filename:
                    score += 12
                    matched_keywords.add(keyword)

                # Path match = strong signal
                if keyword in path:
                    score += 8
                    matched_keywords.add(keyword)

                # Content match
                content_count = content.count(keyword)

                if content_count > 0:
                    # Limit contribution so huge files
                    # don't dominate the ranking.
                    score += min(
                        content_count,
                        5,
                    ) * 2

                    matched_keywords.add(keyword)

                # Language can occasionally help
                if keyword == language:
                    score += 2

            # -------------------------------------------------
            # Bonus for matching multiple different concepts
            # -------------------------------------------------

            if len(matched_keywords) >= 2:
                score += len(matched_keywords) * 2

            # -------------------------------------------------
            # Prefer source code over irrelevant generated files
            # -------------------------------------------------

            ignored_paths = {
                "node_modules",
                ".git",
                "__pycache__",
                "dist",
                "build",
                ".next",
                "coverage",
                "venv",
                ".venv",
            }

            if any(
                ignored in path
                for ignored in ignored_paths
            ):
                score -= 50

            if score > 0:
                scored_files.append(
                    (score, file)
                )

        # Highest score first
        scored_files.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        relevant_files = [
            file
            for score, file in scored_files[:limit]
        ]

        # -----------------------------------------------------
        # Fallback
        # -----------------------------------------------------
        # If keyword search finds nothing, return a few files
        # rather than sending completely empty context to AI.

        if not relevant_files:
            relevant_files = files[:5]

        return relevant_files


    # ---------------------------------------------------------
    # 3. BUILD CONTEXT FOR AI
    # ---------------------------------------------------------

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

            if not content.strip():
                continue

            file_context = (
                f"\n--- FILE: {file.path} ---\n"
                f"Language: {file.language}\n\n"
                f"{content}\n"
            )

            remaining_space = (
                max_characters - current_size
            )

            if remaining_space <= 0:
                break

            if len(file_context) > remaining_space:
                file_context = file_context[
                    :remaining_space
                ]

            context_parts.append(
                file_context
            )

            included_files.append(
                file
            )

            current_size += len(
                file_context
            )

            if current_size >= max_characters:
                break

        return {
            "context": "\n".join(
                context_parts
            ),
            "included_files": included_files,
            "characters": current_size,
        }


    # ---------------------------------------------------------
    # 4. GET SPECIFIC REPOSITORY FILE
    # ---------------------------------------------------------

    @staticmethod
    def get_repository_file(
        db: Session,
        repository_id,
        file_id,
    ):
        file = (
            db.query(ProjectFile)
            .filter(
                ProjectFile.id == file_id,
                ProjectFile.repository_id == repository_id,
            )
            .first()
        )

        return file