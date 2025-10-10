from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.curriculum.models import CurriculumUnit
from src.curriculum.schemas import CurriculumCreate, CurriculumRead

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])

@router.post("/", response_model=CurriculumRead)
def create_unit(payload: CurriculumCreate, db: Session = Depends(get_db)):
    unit = CurriculumUnit(
        title=payload.title,
        subject=payload.subject,
        grade_level=payload.grade_level,
        source_doc=payload.source_doc
    )
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit

@router.get("/", response_model=List[CurriculumRead])
def list_units(db: Session = Depends(get_db)):
    return db.query(CurriculumUnit).all()

@router.get("/{unit_id}", response_model=CurriculumRead)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(CurriculumUnit).filter(CurriculumUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Curriculum unit not found")
    return unit