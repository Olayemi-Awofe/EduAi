# src/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.models import Teacher
from src.auth.schemas import TeacherCreate, TeacherLogin, TeacherRead
from src.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=TeacherRead)
def signup(payload: TeacherCreate, db: Session = Depends(get_db)):
    if db.query(Teacher).filter(Teacher.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    teacher = Teacher(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
        school_id=payload.school_id,
        phone=payload.phone,
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.post("/login")
def login(payload: TeacherLogin, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.email == payload.email).first()
    if not teacher or not verify_password(payload.password, teacher.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": teacher.email})
    return {"access_token": token, "token_type": "bearer"}