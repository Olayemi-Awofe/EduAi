from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from src.database import Base

class CurriculumUnit(Base):
    __tablename__ = "curriculum_units"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    grade_level = Column(String, nullable=False)
    source_doc = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    lessons = relationship("Lesson", back_populates="curriculum_unit", cascade="all, delete-orphan")