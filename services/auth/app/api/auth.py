from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.messaging.publisher import publish_event

from app.core.security import authenticate_user, create_access_token
from app.db.session import get_db
from app.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    # Publicamos el evento en RabbitMQ
    publish_event('UserLoggedIn', {'email': user.email, "token": access_token})
    
    return {"access_token": access_token, "token_type": "bearer"}
