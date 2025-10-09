from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base
from sqlalchemy.dialects.postgresql import JSON

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    curriculum_unit_id = Column(Integer, ForeignKey("curriculum_units.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    topic = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=True)
    content = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    curriculum_unit = relationship("CurriculumUnit", back_populates="lessons")
    teacher = relationship("Teacher", back_populates="lessons")
    assessments = relationship("Assessment", back_populates="lesson", cascade="all, delete-orphan")