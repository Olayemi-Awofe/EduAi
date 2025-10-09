from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship: School -> teachers (back_populates on School)
    school = relationship("School", back_populates="teachers")
    lessons = relationship("Lesson", back_populates="teacher", cascade="all, delete-orphan")
    progress = relationship("TeacherProgress", back_populates="teacher", cascade="all, delete-orphan")