from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeacherProgressCreate(BaseModel):
    teacher_id: int
    skill: str
    progress: int
    last_practiced: Optional[datetime] = None

class TeacherProgressRead(BaseModel):
    id: int
    teacher_id: int
    skill: str
    progress: int
    last_practiced: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True