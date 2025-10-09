from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class LessonCreate(BaseModel):
    curriculum_unit_id: Optional[int] = None
    teacher_id: Optional[int] = None
    topic: str
    subject: str
    grade: int
    duration: Optional[int] = None
    no_of_questions: int
    lesson_outcome: str

class LessonRead(BaseModel):
    id: int
    curriculum_unit_id: Optional[int]
    teacher_id: Optional[int]
    topic: str
    subject: str
    grade: int
    duration: Optional[int]
    content: dict[str, Any]
    created_at: datetime

    class Config:
        orm_mode = True