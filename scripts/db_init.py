from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum
import os

# ---------- Database setup ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "edu_ai.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
Base = declarative_base()


# ---------- Enum types ----------
class TechLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class DeviceType(enum.Enum):
    basic = "basic"
    smartphone = "smartphone"
    laptop = "laptop"


class Connectivity(enum.Enum):
    offline = "offline"
    intermittent = "intermittent"
    online = "online"


# ---------- Table definitions ----------
class School(Base):
    __tablename__ = "schools"
    id = Column(String, primary_key=True)
    name = Column(String)
    region = Column(String)
    device_type = Column(Enum(DeviceType))
    connectivity = Column(Enum(Connectivity))

    teachers = relationship("Teacher", back_populates="school")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    school_id = Column(String, ForeignKey("schools.id"))
    languages = Column(JSON)
    tech_level = Column(Enum(TechLevel))
    created_at = Column(DateTime, default=datetime.utcnow)

    school = relationship("School", back_populates="teachers")


class CurriculumUnit(Base):
    __tablename__ = "curriculum_units"
    id = Column(String, primary_key=True)
    title = Column(String)
    subject = Column(String)
    grade_level = Column(String)
    source_doc = Column(String)
    canonical_learning_outcomes = Column(JSON)


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(String, primary_key=True)
    curriculum_unit_id = Column(String, ForeignKey("curriculum_units.id"))
    teacher_id = Column(String, ForeignKey("teachers.id"))
    content = Column(JSON)
    assets = Column(JSON)
    lesson_metadata = Column(JSON)
    generated_at = Column(DateTime, default=datetime.utcnow)


class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(String, primary_key=True)
    lesson_id = Column(String, ForeignKey("lessons.id"))
    items = Column(JSON)


class TeacherProgress(Base):
    __tablename__ = "teacher_progress"
    id = Column(String, primary_key=True)
    teacher_id = Column(String, ForeignKey("teachers.id"))
    skill = Column(String)
    level = Column(String)
    last_practiced = Column(DateTime)


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    action = Column(String)
    prompt_hash = Column(String)
    model_used = Column(String)
    output_ref = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ---------- Create all tables ----------
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(f"Database created successfully at {DB_PATH}")
