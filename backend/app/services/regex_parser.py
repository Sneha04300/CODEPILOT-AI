import re

from app.schemas.resume import ResumeData, Project, Experience, Education


class RegexParser:

    @staticmethod
    def parse_resume(text: str) -> ResumeData:
        return ResumeData(
            skills=RegexParser._extract_skills(text),
            projects=RegexParser._extract_projects(text),
            experience=RegexParser._extract_experience(text),
            education=RegexParser._extract_education(text),
        )

    @staticmethod
    def _extract_skills(text: str) -> list[str]:
        section = RegexParser._extract_section(text, r"(?:TECHNICAL\s+)?SKILLS?")
        if not section:
            return []
        skills = re.split(r"[,•\|\n]+", section)
        return sorted(
            {s.strip() for s in skills if len(s.strip()) > 1}
        )

    @staticmethod
    def _extract_projects(text: str) -> list[Project]:
        section = RegexParser._extract_section(text, r"PROJECTS?")
        if not section:
            return []
        projects: list[Project] = []
        lines = section.strip().split("\n")
        current_name = ""
        current_desc: list[str] = []
        current_techs: list[str] = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            tech_match = re.match(
                r"^(?:Technologies|Tech Stack|Tools|Stack)\s*[:\-]\s*(.+)",
                line,
                re.IGNORECASE,
            )
            if tech_match:
                current_techs = [
                    t.strip()
                    for t in re.split(r"[,•\|\n]+", tech_match.group(1))
                    if t.strip()
                ]
                continue
            if re.match(r"^[A-Z][A-Za-z0-9\s\-]{2,}(?::|–|—|$)", line):
                if current_name:
                    projects.append(
                        Project(
                            name=current_name,
                            description=" ".join(current_desc).strip(),
                            technologies=current_techs,
                        )
                    )
                    current_desc = []
                    current_techs = []
                current_name = line.rstrip(":–—")
            else:
                current_desc.append(line)

        if current_name:
            projects.append(
                Project(
                    name=current_name,
                    description=" ".join(current_desc).strip(),
                    technologies=current_techs,
                )
            )
        return projects

    @staticmethod
    def _extract_experience(text: str) -> list[Experience]:
        section = RegexParser._extract_section(
            text, r"(?:EXPERIENCE|EMPLOYMENT|WORK\s+HISTORY|WORK EXPERIENCE)"
        )
        if not section:
            return []
        experiences: list[Experience] = []
        lines = section.strip().split("\n")
        current_company = ""
        current_role = ""
        current_duration = ""
        current_desc: list[str] = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            company_match = re.match(
                r"^(.+?)\s*(?:–|—|-)\s*(.+?)(?:\s*(?:–|—|-)\s*(.+))?$",
                line,
            )
            if company_match:
                if current_company:
                    experiences.append(
                        Experience(
                            company=current_company,
                            role=current_role,
                            duration=current_duration,
                            description=" ".join(current_desc).strip(),
                        )
                    )
                    current_desc = []
                current_company = company_match.group(1).strip()
                current_role = company_match.group(2).strip()
                current_duration = (
                    company_match.group(3).strip() if company_match.group(3) else ""
                )
                continue
            date_match = re.match(
                r"^([A-Z][a-z]+\.?\s*\d{4})\s*(?:–|—|-)\s*([A-Z][a-z]+\.?\s*\d{4}|Present)",
                line,
            )
            if date_match:
                current_duration = line.strip()
                continue
            current_desc.append(line)

        if current_company:
            experiences.append(
                Experience(
                    company=current_company,
                    role=current_role,
                    duration=current_duration,
                    description=" ".join(current_desc).strip(),
                )
            )
        return experiences

    @staticmethod
    def _extract_education(text: str) -> list[Education]:
        section = RegexParser._extract_section(text, r"EDUCATION")
        if not section:
            return []
        education_list: list[Education] = []
        lines = section.strip().split("\n")
        current_institution = ""
        current_degree = ""
        current_field = ""
        current_year = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            year_match = re.search(r"(\d{4})\s*(?:–|—|-)\s*(\d{4}|Present)", line)
            if year_match:
                current_year = line.strip()
                continue
            degree_match = re.match(
                r"^(Bachelor(?:'s)?|Master(?:'s)?|PhD|Doctorate|B\.\w+|M\.\w+|B\.?E\.?|B\.?Tech|M\.?Tech|B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?B\.?A\.?|Associate)\s+(?:of\s+|in\s+)?(.+)",
                line,
                re.IGNORECASE,
            )
            if degree_match:
                current_degree = degree_match.group(1).strip()
                rest = degree_match.group(2).strip()
                field_match = re.match(
                    r"(.+?)(?:\s*(?:–|—|-)\s*(.+))?$", rest
                )
                if field_match:
                    current_field = field_match.group(1).strip()
                    if field_match.group(2):
                        if not current_institution:
                            current_institution = field_match.group(2).strip()
                continue
            if re.match(r"^[A-Z][A-Za-z\s]+(?:University|College|Institute|School)", line):
                if current_institution and current_degree:
                    education_list.append(
                        Education(
                            institution=current_institution,
                            degree=current_degree,
                            field=current_field,
                            graduation_year=current_year,
                        )
                    )
                    current_degree = ""
                    current_field = ""
                    current_year = ""
                current_institution = line.strip()

        if current_institution and current_degree:
            education_list.append(
                Education(
                    institution=current_institution,
                    degree=current_degree,
                    field=current_field,
                    graduation_year=current_year,
                )
            )
        return education_list

    @staticmethod
    def _extract_section(text: str, header_pattern: str) -> str | None:
        pattern = re.compile(
            rf"(?:^|\n)\s*{header_pattern}\s*(?:\n|$)(.*?)(?=\n\s*(?:{'|'.join([
                r'TECHNICAL\s+SKILLS',
                r'SKILLS?',
                r'PROJECTS?',
                r'EXPERIENCE',
                r'EMPLOYMENT',
                r'WORK\s+HISTORY',
                r'WORK EXPERIENCE',
                r'EDUCATION',
                r'CERTIFICATIONS?',
                r'ACHIEVEMENTS?',
                r'SUMMARY',
                r'OBJECTIVE',
                r'LANGUAGES',
                r'INTERESTS?',
                r'REFERENCES?',
            ])})\s*(?:\n|$)|\Z)",
            re.IGNORECASE | re.DOTALL,
        )
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return None
