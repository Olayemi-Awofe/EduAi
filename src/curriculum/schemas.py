from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CurriculumCreate(BaseModel):
    title: str
    subject: str
    grade_level: str
    source_doc: Optional[str] = None

class CurriculumRead(BaseModel):
    id: int
    title: str
    subject: str
    grade_level: str
    source_doc: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True