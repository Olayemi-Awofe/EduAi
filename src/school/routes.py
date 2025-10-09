from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.school.models import School
from src.school.schemas import SchoolCreate, SchoolRead

router = APIRouter(prefix="/schools", tags=["Schools"])

@router.post("/", response_model=SchoolRead)
def create_school(payload: SchoolCreate, db: Session = Depends(get_db)):
    school = School(
        name=payload.name,
        region=payload.region,
        device_type=payload.device_type,
        connectivity=payload.connectivity
    )
    db.add(school)
    db.commit()
    db.refresh(school)
    return school

@router.get("/", response_model=List[SchoolRead])
def list_schools(db: Session = Depends(get_db)):
    return db.query(School).all()

@router.get("/{school_id}", response_model=SchoolRead)
def get_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school