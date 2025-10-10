from sqlalchemy import (
    Column, Integer, String, Boolean, Float, ForeignKey, DateTime, JSON, Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database import Base


class SkillLevel(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    level = Column(Enum(SkillLevel), nullable=False)
    total_sections = Column(Integer, default=0)
    category = Column(String)
    estimated_duration = Column(String)
    thumbnail_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    teacher = relationship("Teacher", back_populates="skills")
    sections = relationship("Section", back_populates="skill", cascade="all, delete-orphan")
    tests = relationship("Test", back_populates="skill", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="skill", cascade="all, delete-orphan")
    progress_records = relationship("TeacherSkillProgress", back_populates="skill", cascade="all, delete-orphan")


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    order = Column(Integer)
    title = Column(String)
    content = Column(String)
    video_url = Column(String)
    resource_url = Column(String)
    duration = Column(String)
    quiz_included = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    skill = relationship("Skill", back_populates="sections")
    teacher = relationship("Teacher", back_populates="sections")


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    status = Column(String, default="pending")
    score = Column(Float, default=0)
    total_questions = Column(Integer, default=0)
    time_limit = Column(Integer)
    attempts = Column(Integer, default=0)

    skill = relationship("Skill", back_populates="tests")
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")
    teacher = relationship("Teacher", back_populates="tests")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    question = Column(String)
    question_type = Column(String, default="multiple_choice")
    options = Column(JSON)
    correct_answer = Column(String)
    user_answer = Column(String)
    correct = Column(Boolean, default=False)
    explanation = Column(String)
    difficulty = Column(String)

    skill = relationship("Skill", back_populates="questions")
    test = relationship("Test", back_populates="questions")
    teacher = relationship("Teacher", back_populates="questions")


class TeacherSkillProgress(Base):
    __tablename__ = "teacher_skill_progress"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    completed_sections = Column(Integer, default=0)
    progress = Column(Float, default=0)
    completed = Column(Boolean, default=False)
    score = Column(Float, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    last_accessed_section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)

    skill = relationship("Skill", back_populates="progress_records")
    teacher = relationship("Teacher", back_populates="progress_records")
    last_section = relationship("Section")