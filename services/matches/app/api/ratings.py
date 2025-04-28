from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session, select
from typing import List, Optional
import httpx

from app.db.models import Match, Rating
from app.db.session import get_db
from app.schemas.rating import RatingCreate, RatingRead, RatingUpdate, TopRatedMatch
from app.core.config import settings 

router = APIRouter()

async def get_current_user(token: str) -> int:
    """ Obtener el ID del usuario actual desde el token de autenticación"""
    try:
       async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.AUTH_SERVICE_URL}/users/me", headers={"Authorization": f"Bearer {token}"})

            if response.status_code == 200:
               user = response.json
               return user["id"]

            return None

    except httpx.RequestError:
        return None

        
@router.post("/", response_model=RatingRead, status_code=status.HTTP_201_CREATED)
async def rate_match(rating_data: RatingCreate, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated"
        )

    token = authorization.replace("Bearer", "")
    user_id = await get_current_user(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Verificamos que la lucha existe
    statement = select(Match).where(Match.id == rating_data.match_id)
    match = db.exec(statement).first()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    # Verificamos si el usuario ya ha calificado esta lucha.
    statement = select(Rating).where(Rating.match_id == rating_data.match_id, Rating.user_id == user_id)
    existing_rating = db.exec(statement).first()

    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already rated this match"
        )

    # Creamos el rating 
    db_rating = Rating(
        match_id=rating_data.match_id,
        user_id=user_id,
        rating=rating_data.rating,
        comment=rating_data.comment
    )

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return db_rating

    
@router.get("/match/{match_id}", response_model=List[RatingRead])
def get_match_ratings(match_id: int, db: Session = Depends(get_db)):
    
    # Verificamos que la lucha exista
    statement = select(Match).where(Match.id == match_id)
    match = db.exec(statement).first()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    statement = select(Rating).where(Rating.match_id == match_id).all()
    ratings = db.exec(statement)

    return ratings 
    