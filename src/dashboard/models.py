from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from src.database import Base

class TeacherMonthlyAnalytics(Base):
    __tablename__ = "teacher_monthly_analytics"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    lesson = Column(Integer, default=0)
    upskilling = Column(Integer, default=0)
    month = Column(String, nullable=False)  # format: "Jan-2025"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())