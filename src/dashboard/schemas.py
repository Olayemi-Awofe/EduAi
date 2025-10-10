from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeacherMonthlyAnalyticsCreate(BaseModel):
    teacher_id: int

class TeacherMonthlyAnalyticsOut(BaseModel):
    id: int
    teacher_id: int
    lesson: int
    upskilling: int
    month: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True