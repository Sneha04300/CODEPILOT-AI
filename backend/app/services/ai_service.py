from groq import Groq

from app.core.config import GROQ_API_KEY


class AIService:

    @staticmethod
    def ask_repository(
        question: str,
        context: str,
        history=None,
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

        # Add previous conversation history
        if history:
            for message in history:
                if message.role not in ("user", "assistant"):
                    continue

                messages.append(
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                )

        # Add repository context + current question
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

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2,
        )

        answer = completion.choices[0].message.content

        if not answer:
            return "No response was generated."

        return answer.strip()