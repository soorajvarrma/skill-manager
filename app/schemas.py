"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    name: str


class SkillBase(BaseModel):
    """Base schema for skill."""
    name: str
    level: int = Field(ge=1, le=5, description="Skill level from 1 to 5")


class SkillCreate(SkillBase):
    """Schema for creating a new skill."""
    pass


class SkillUpdate(BaseModel):
    """Schema for updating a skill."""
    level: int = Field(ge=1, le=5)


class Skill(SkillBase):
    """Schema for skill response."""
    id: int
    user_id: int

    class Config:
        from_attributes = True


class CertificationBase(BaseModel):
    """Base schema for certification."""
    name: str
    issuer: str
    date_obtained: str


class CertificationCreate(CertificationBase):
    """Schema for creating a new certification."""
    pass


class Certification(CertificationBase):
    """Schema for certification response."""
    id: int
    user_id: int

    class Config:
        from_attributes = True


class AchievementBase(BaseModel):
    """Base schema for achievement."""
    title: str
    description: str
    date: str


class AchievementCreate(AchievementBase):
    """Schema for creating a new achievement."""
    pass


class Achievement(AchievementBase):
    """Schema for achievement response."""
    id: int
    user_id: int

    class Config:
        from_attributes = True


class User(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    name: str
    created_at: datetime
    skills: List[Skill] = []
    certifications: List[Certification] = []
    achievements: List[Achievement] = []

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    """Schema for creating a new role."""
    name: str
    requirements: Dict[str, int]


class Role(BaseModel):
    """Schema for role response."""
    id: int
    name: str
    requirements: Dict[str, int]

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    """Schema for creating a new course."""
    title: str
    provider: str
    level: str
    related_skill: str


class Course(BaseModel):
    """Schema for course response."""
    id: int
    title: str
    provider: str
    level: str
    related_skill: str

    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    """Schema for skill gap analysis request."""
    user_id: int
    role: str


class AnalysisResponse(BaseModel):
    """Schema for skill gap analysis response."""
    analysis: Dict[str, Any]
    recommendations: List[Dict[str, str]]
    study_plan: str
    ai_used: bool


class QuizQuestion(BaseModel):
    """Schema for a quiz question."""
    q: str
    options: List[str]
    correct: int
    difficulty: str


class QuizResponse(BaseModel):
    """Schema for quiz generation response."""
    skill: str
    questions: List[QuizQuestion]


class QuizSubmission(BaseModel):
    """Schema for quiz answer submission."""
    answers: List[int]


class QuizResult(BaseModel):
    """Schema for quiz result."""
    score: int
    suggested_level: int
    ai_used: bool
    detailed_results: Optional[List[Dict[str, Any]]] = None