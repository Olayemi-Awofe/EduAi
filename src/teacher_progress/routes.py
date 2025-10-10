from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.teacher_progress.models import TeacherProgress
from src.teacher_progress.schemas import TeacherProgressCreate, TeacherProgressRead

router = APIRouter(prefix="/teacher-progress", tags=["TeacherProgress"])

@router.post("/", response_model=TeacherProgressRead)
def create_progress(payload: TeacherProgressCreate, db: Session = Depends(get_db)):
    tp = TeacherProgress(
        teacher_id=payload.teacher_id,
        skill=payload.skill,
        progress=payload.progress,
        last_practiced=payload.last_practiced
    )
    db.add(tp)
    db.commit()
    db.refresh(tp)
    return tp

@router.get("/by-teacher/{teacher_id}", response_model=List[TeacherProgressRead])
def get_progress_for_teacher(teacher_id: int, db: Session = Depends(get_db)):
    return db.query(TeacherProgress).filter(TeacherProgress.teacher_id == teacher_id).all()

@router.put("/{progress_id}", response_model=TeacherProgressRead)
def update_progress(progress_id: int, payload: TeacherProgressCreate, db: Session = Depends(get_db)):
    tp = db.query(TeacherProgress).filter(TeacherProgress.id == progress_id).first()
    if not tp:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(tp, k, v)
    db.commit()
    db.refresh(tp)
    return tp