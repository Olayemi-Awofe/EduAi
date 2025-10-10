from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class TeacherProgress(Base):
    __tablename__ = "teacher_progress"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    skill = Column(String, nullable=False)
    progress = Column(Integer, nullable=False, default=0)
    last_practiced = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("Teacher", back_populates="progress")