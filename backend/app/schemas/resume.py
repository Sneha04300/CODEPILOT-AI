from pydantic import BaseModel
from typing import List, Optional


class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = []


class Experience(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    field: Optional[str] = None
    graduation_year: Optional[str] = None


class ResumeData(BaseModel):
    skills: List[str] = []
    projects: List[Project] = []
    experience: List[Experience] = []
    education: List[Education] = []


class ResumeResponse(BaseModel):
    success: bool
    data: Optional[ResumeData] = None
    source: str
    message: Optional[str] = None
