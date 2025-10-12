from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AssessmentCreate(BaseModel):
    lesson_id: int
    content: dict[str, Any]

class AssessmentRead(BaseModel):
    id: int
    lesson_id: int
    content: dict[str, Any]
    created_at: datetime

    class Config:
        orm_mode = True