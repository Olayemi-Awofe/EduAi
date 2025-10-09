from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SchoolCreate(BaseModel):
    name: str
    region: str
    device_type: Optional[str] = None
    connectivity: Optional[str] = None

class SchoolRead(BaseModel):
    id: int
    name: str
    region: str
    device_type: Optional[str]
    connectivity: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True