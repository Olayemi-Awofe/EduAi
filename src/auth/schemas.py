# src/auth/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    school_id: Optional[int] = None
    phone: Optional[str] = None

class TeacherLogin(BaseModel):
    email: EmailStr
    password: str

class TeacherRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    school_id: Optional[int]
    phone: Optional[str]

    class Config:
        orm_mode = True