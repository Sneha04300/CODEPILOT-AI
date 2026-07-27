from groq import Groq

from app.core.config import GROQ_API_KEY


class AIService:

    # Maximum previous messages sent to Groq
    MAX_HISTORY_MESSAGES = 12

    @staticmethod
    def ask_repository(
        question: str,
        context: str,
        history=None,
    ) -> str:

        # -----------------------------------------------------
        # 1. Validate API key
        # -----------------------------------------------------

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        # -----------------------------------------------------
        # 2. Validate question
        # -----------------------------------------------------

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        # -----------------------------------------------------
        # 3. Prepare Groq client
        # -----------------------------------------------------

        try:
            client = Groq(
                api_key=GROQ_API_KEY
            )

        except Exception as error:
            raise RuntimeError(
                "Failed to initialize AI service."
            ) from error

        system_prompt = """
You are CodePilot AI, an AI assistant that helps developers understand
software repositories.

Answer the user's question using the provided repository code and
previous conversation when relevant.

Rules:
1. Base technical claims on the repository context.
2. Do not invent files, functions, classes, or behavior.
3. Mention relevant filenames when useful.
4. Explain code clearly and technically.
5. If the repository context is insufficient, say so.
6. Use previous conversation messages to understand follow-up questions.
7. Do not treat previous assistant answers as repository evidence.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # -----------------------------------------------------
        # 4. Add limited conversation history
        # -----------------------------------------------------

        if history:

            valid_history = [
                message
                for message in history
                if message.role in (
                    "user",
                    "assistant",
                )
            ]

            recent_history = valid_history[
                -AIService.MAX_HISTORY_MESSAGES:
            ]

            for message in recent_history:

                if not message.content:
                    continue

                messages.append(
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                )

        # -----------------------------------------------------
        # 5. Prepare repository context
        # -----------------------------------------------------

        if not context or not context.strip():
            context = (
                "No relevant repository context "
                "was available for this question."
            )

        current_prompt = f"""
REPOSITORY CONTEXT:

{context}

CURRENT USER QUESTION:

{question}
"""

        messages.append(
            {
                "role": "user",
                "content": current_prompt,
            }
        )

        # -----------------------------------------------------
        # 6. Call Groq
        # -----------------------------------------------------

        try:

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.2,
            )

        except Exception as error:

            raise RuntimeError(
                "AI service is currently unavailable."
            ) from error

        # -----------------------------------------------------
        # 7. Validate AI response
        # -----------------------------------------------------

        if (
            not completion
            or not completion.choices
        ):
            raise RuntimeError(
                "AI service returned an invalid response."
            )

        answer = (
            completion
            .choices[0]
            .message
            .content
        )

        if not answer or not answer.strip():
            raise RuntimeError(
                "AI service returned an empty response."
            )

        return answer.strip()