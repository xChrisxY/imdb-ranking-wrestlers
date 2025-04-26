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
    match = select(Match).where(Match.id == rating_data.match_id).first()