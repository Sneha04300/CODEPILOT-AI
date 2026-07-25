from groq import Groq

from app.core.config import GROQ_API_KEY


class AIService:

    @staticmethod
    def ask_repository(
        question: str,
        context: str,
    ) -> str:

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        client = Groq(
            api_key=GROQ_API_KEY
        )

        system_prompt = """
You are CodePilot AI, an AI assistant that helps developers understand
software repositories.

Answer the user's question using the provided repository code.

Rules:
1. Base your answer on the repository context.
2. Do not invent files, functions, classes, or behavior.
3. Mention relevant filenames when useful.
4. Explain code clearly and technically.
5. If the provided context is insufficient, say so.
"""

        user_prompt = f"""
REPOSITORY CONTEXT:

{context}

USER QUESTION:

{question}
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
        )

        answer = completion.choices[0].message.content

        if not answer:
            return "No response was generated."

        return answer.strip()