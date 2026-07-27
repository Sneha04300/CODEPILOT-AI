import re


class StaticAnalysisService:

    @staticmethod
    def analyze_file(file):
        findings = []

        content = file.content or ""

        if not content.strip():
            return findings

        lines = content.splitlines()

        # -------------------------------------------------
        # 1. POSSIBLE HARDCODED SECRETS
        # -------------------------------------------------

        secret_pattern = re.compile(
            r"""(?i)
            (api[_-]?key|
             secret[_-]?key|
             access[_-]?token|
             auth[_-]?token|
             password)
            \s*[:=]\s*
            ["'][^"']+["']
            """,
            re.VERBOSE,
        )

        for line_number, line in enumerate(
            lines,
            start=1,
        ):
            if secret_pattern.search(line):
                findings.append(
                    {
                        "file_id": file.id,
                        "category": "security",
                        "severity": "high",
                        "title": "Possible hardcoded secret",
                        "description": (
                            "A possible credential or secret "
                            "is stored directly in source code."
                        ),
                        "recommendation": (
                            "Store sensitive values in "
                            "environment variables or a "
                            "secret manager."
                        ),
                        "line_number": line_number,
                    }
                )

        # -------------------------------------------------
        # 2. DEBUG PRINT STATEMENTS
        # -------------------------------------------------

        if file.language == "python":

            for line_number, line in enumerate(
                lines,
                start=1,
            ):
                stripped = line.strip()

                if stripped.startswith("print("):
                    findings.append(
                        {
                            "file_id": file.id,
                            "category": "quality",
                            "severity": "low",
                            "title": "Debug print statement",
                            "description": (
                                "A print statement was found "
                                "in Python source code."
                            ),
                            "recommendation": (
                                "Use structured logging for "
                                "application diagnostics."
                            ),
                            "line_number": line_number,
                        }
                    )

        # -------------------------------------------------
        # 3. TODO / FIXME COMMENTS
        # -------------------------------------------------

        for line_number, line in enumerate(
            lines,
            start=1,
        ):
            upper_line = line.upper()

            if "TODO" in upper_line or "FIXME" in upper_line:
                findings.append(
                    {
                        "file_id": file.id,
                        "category": "quality",
                        "severity": "low",
                        "title": "Unresolved TODO/FIXME",
                        "description": (
                            "The source file contains an "
                            "unfinished TODO or FIXME marker."
                        ),
                        "recommendation": (
                            "Review the marked code and "
                            "resolve or document the pending work."
                        ),
                        "line_number": line_number,
                    }
                )

        return findings