from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.lesson.models import Lesson
from src.lesson.schemas import LessonCreate, LessonRead
from src.database import SessionLocal
from src.lesson import schemas, models
from src.assessments.models import Assessment
from src.core.security import get_current_teacher
from utils import generate_lessons_with_assessment

router = APIRouter(prefix="/lessons", tags=["Lessons"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.LessonRead)
def create_lesson(
    lesson: schemas.LessonCreate,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    topic = lesson.topic
    subject = lesson.subject
    grade = lesson.grade
    duration = lesson.duration
    lesson_outcome = lesson.lesson_outcome
    no_of_questions = lesson.no_of_questions
    response = generate_lessons_with_assessment(topic, subject, grade, duration, lesson_outcome, no_of_questions)

    db_lesson = models.Lesson(
        curriculum_unit_id=lesson.curriculum_unit_id,
        teacher_id=current_teacher.id,
        topic=lesson.topic,
        subject=lesson.subject,
        grade=lesson.grade,
        duration=lesson.duration,
        content=response["lesson"],
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)

    #saving data to assessment
    db_assessment = Assessment(
        lesson_id=db_lesson.id,
        content=response["assessment"]
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_lesson


@router.get("/", response_model=list[schemas.LessonRead])
def get_lessons(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    lessons = db.query(models.Lesson).filter(models.Lesson.teacher_id == current_teacher.id).all()
    return lessons

@router.get("/{lesson_id}", response_model=LessonRead)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if lesson.teacher_id != current_teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this lesson")
    return lesson


@router.put("/{lesson_id}", response_model=LessonRead)
def update_lesson(
    lesson_id: int,
    payload: LessonCreate,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if lesson.teacher_id != current_teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this lesson")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(lesson, key, value)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if lesson.teacher_id != current_teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this lesson")

    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}