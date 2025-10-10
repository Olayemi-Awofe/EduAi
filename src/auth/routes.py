from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.models import Teacher
from src.auth.schemas import TeacherCreate, TeacherRead
from src.core.security import hash_password
from src.auth.schemas import TeacherLogin
from src.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=TeacherRead)
def signup(payload: TeacherCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_teacher = db.query(Teacher).filter(Teacher.email == payload.email).first()
    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Optional: Check if phone number already exists
    existing_phone = db.query(Teacher).filter(Teacher.phone == payload.phone).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    try:
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create account: {str(e)}"
        )


@router.post("/login")
def login(payload: TeacherLogin, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.email == payload.email).first()

    if not teacher:
        # Email not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email address or password"
        )

    if not verify_password(payload.password, teacher.password):
        # Password is wrong
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    token = create_access_token({"sub": teacher.email})

    return {
        "email": teacher.email,
        "name": teacher.name,
        "token": token
    }