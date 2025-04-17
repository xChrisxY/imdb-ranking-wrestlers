from fastapi import APIRouter, Depends, HTTPException, status 
from sqlmodel import Session, select
from typing import List

from app.core.security import get_password_hash, get_current_user
from app.db.models import User 
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    statement = select(User).where(User.email == user.email)
    db_user = db.exec(statement).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    statement = select(User).where(User.username == user.username)
    db_user = db.exec(statement).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Ahora si creamos el usuario
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, username=user.username, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user