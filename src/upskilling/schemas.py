from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


# ===== Enum =====
class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


# ====== Skill ======
class SkillBase(BaseModel):
    title: str
    description: Optional[str]
    level: SkillLevel
    total_sections: int
    category: Optional[str]
    estimated_duration: Optional[str]
    thumbnail_url: Optional[str]


class SkillCreate(SkillBase):
    title: str
    level: str
    description: Optional[str] = None
    total_sections: Optional[int] = None
    category: Optional[str] = None
    estimated_duration: Optional[str] = None
    thumbnail_url: Optional[str] = None


class SkillOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    level: SkillLevel
    category: Optional[str]
    total_sections: int
    estimated_duration: Optional[str]
    thumbnail_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True




# ====== Section ======
class SectionBase(BaseModel):
    order: Optional[int]
    title: str
    content: str
    video_url: Optional[str]
    resource_url: Optional[str]
    duration: Optional[str]
    quiz_included: Optional[bool] = False
    completed: Optional[bool] = False


class SectionCreate(SectionBase):
    skill_id: int


class SectionOut(SectionBase):
    id: int
    order: Optional[int]
    title: Optional[str]
    content: Optional[str]
    video_url: Optional[str]
    resource_url: Optional[str]
    duration: Optional[str]
    quiz_included: Optional[bool]
    completed: Optional[bool]

    class Config:
        orm_mode = True

class QuestionOut(BaseModel):
    id: int
    question: str
    options: Optional[dict]
    correct_answer: Optional[str]
    explanation: Optional[str]
    difficulty: Optional[str]

    class Config:
        orm_mode = True

# ====== Test ======
class TestBase(BaseModel):
    status: Optional[str] = "pending"
    score: Optional[float] = 0
    total_questions: Optional[int] = 0
    time_limit: Optional[int]
    attempts: Optional[int] = 0


class TestCreate(TestBase):
    skill_id: int


class TestOut(BaseModel):
    id: int
    status: str
    total_questions: int
    time_limit: Optional[int]
    attempts: Optional[int]
    questions: List[QuestionOut] = []

    class Config:
        orm_mode = True


# ====== Question ======
class QuestionBase(BaseModel):
    question: str
    question_type: Optional[str] = "multiple_choice"
    options: Any
    correct_answer: str
    user_answer: Optional[str]
    correct: Optional[bool] = False
    explanation: Optional[str]
    difficulty: Optional[str]


class QuestionCreate(QuestionBase):
    skill_id: int
    test_id: int



# ====== Progress ======
class TeacherSkillProgressBase(BaseModel):
    completed_sections: Optional[int] = 0
    progress: Optional[float] = 0
    completed: Optional[bool] = False
    score: Optional[float] = 0


class TeacherSkillProgressCreate(TeacherSkillProgressBase):
    skill_id: int


class TeacherSkillProgressOut(TeacherSkillProgressBase):
    progress: int

    class Config:
        orm_mode = True


class SkillRead(SkillOut):
    sections: list[SectionOut] = []
    test: Optional[TestOut] = None
    progress_record: Optional[TeacherSkillProgressOut] = None