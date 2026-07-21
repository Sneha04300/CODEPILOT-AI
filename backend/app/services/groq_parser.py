import json

from groq import Groq

from app.core.config import GROQ_API_KEY


class GroqParser:

    @staticmethod
    def parse_resume(text: str) -> dict | None:
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            return None

        client = Groq(api_key=GROQ_API_KEY)

        prompt = (
            "You are a resume parser. Extract structured information from the following resume text. "
            "Return ONLY valid JSON with this exact structure, no markdown, no extra text:\n"
            "{\n"
            '  "skills": ["Skill1", "Skill2", ...],\n'
            '  "projects": [\n'
            '    {"name": "...", "description": "...", "technologies": ["Tech1", ...]}\n'
            "  ],\n"
            '  "experience": [\n'
            '    {"company": "...", "role": "...", "duration": "...", "description": "..."}\n'
            "  ],\n"
            '  "education": [\n'
            '    {"institution": "...", "degree": "...", "field": "...", "graduation_year": "..."}\n'
            "  ]\n"
            "}\n\n"
            "If a section has no data, use an empty array. "
            "Use empty strings for missing fields.\n\n"
            f"Resume text:\n{text}"
        )

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a resume parser that outputs only valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )

            content = completion.choices[0].message.content.strip()

            if content.startswith("```"):
                content = content.split("\n", 1)[-1]
                content = content.rsplit("```", 1)[0]
                content = content.strip()

            return json.loads(content)

        except Exception:
            return None
