from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.lesson.models import Lesson
from src.assessments.models import Assessment
from src.core.security import get_current_teacher

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/analytics")
def get_teacher_dashboard(db: Session = Depends(get_db), current_teacher = Depends(get_current_teacher)):
    total_lessons = db.query(Lesson).filter(Lesson.teacher_id == current_teacher.id).count()
    total_assessments = db.query(Assessment).join(Lesson).filter(Lesson.teacher_id == current_teacher.id).count()

    return {
        "total_lessons": total_lessons,
        "total_assessments": total_assessments
    }