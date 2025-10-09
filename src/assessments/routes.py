from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.database import get_db
from src.assessments.models import Assessment
from src.assessments.schemas import AssessmentCreate, AssessmentRead

router = APIRouter(prefix="/assessments", tags=["Assessments"])

@router.post("/", response_model=AssessmentRead)
def create_assessment(payload: AssessmentCreate, db: Session = Depends(get_db)):
    assessment = Assessment(lesson_id=payload.lesson_id, content=payload.content)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

@router.get("/", response_model=List[AssessmentRead])
def list_assessments(db: Session = Depends(get_db)):
    return db.query(Assessment).all()

@router.get("/{assessment_id}", response_model=AssessmentRead)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return a

@router.get("/by-lesson/{lesson_id}", response_model=List[AssessmentRead])
def assessments_by_lesson(lesson_id: int, db: Session = Depends(get_db)):
    return db.query(Assessment).filter(Assessment.lesson_id == lesson_id).all()