from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from src.database import SessionLocal
from src.auth.models import Teacher
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from src.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    password = password.encode("utf-8")[:72]  # truncate safely
    return pwd_context.hash(password.decode("utf-8"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(plain_password.decode("utf-8"), hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_teacher(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        teacher_email: str = payload.get("sub")
        if teacher_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = SessionLocal()
    teacher = db.query(Teacher).filter(Teacher.email == teacher_email).first()
    db.close()
    if teacher is None:
        raise credentials_exception
    return teacher
