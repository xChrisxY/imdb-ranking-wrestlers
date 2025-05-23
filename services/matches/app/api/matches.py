from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session, select, func
from typing import List, Optional, Dict 
import httpx 
from datetime import datetime, timezone, timedelta 

from app.db.models import Match, Rating, MatchWrestler, MatchType
from app.db.session import get_db 
from app.schemas.match import MatchCreate, MatchRead, MatchDetail, MatchUpdate
from app.core.config import settings 

router = APIRouter()

async def get_wrestler_info(wrestler_id: int):
    """ Obtenemos información de un luchador del servicio wrestlers """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.WRESTLERS_SERVICE_URL}/wrestlers/{wrestler_id}")
            print(response)
            if response.status_code == 200:
                return response.json()
            return None
            
    except httpx.RequestError:
        return None

async def get_event_info(event_id: int):
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.EVENTS_SERVICE_URL}/events/{event_id}")
            if response.status_code == 200:
                return response.json()
            return None
    except httpx.RequestError:
        return None 

        
@router.post("/", response_model=MatchRead, status_code=status.HTTP_201_CREATED)
async def create_match(match_data: MatchCreate, db: Session = Depends(get_db)):
    
    # Verificamos si el evento existe
    event_info = await get_event_info(match_data.event_id)
    if not event_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # verificamos que los luchadores existan
    for wrestler_entry in match_data.wrestlers:
        wrestler_info = await get_wrestler_info(wrestler_entry.wrestler_id)
        if not wrestler_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wrestler with ID {wrestler_entry.wrestler_id} not found"
            )

    # Creamos la lucha 
    db_match = Match(
        event_id=match_data.event_id,
        match_type=match_data.match_type,
        title_match=match_data.title_match,
        duration=match_data.duration,
        match_date=match_data.match_date,
        description=match_data.description,
        main_event=match_data.main_event
    )

    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    # Agregar los luchadores a la lucha
    for wrestler_entry in match_data.wrestlers:
        match_wrestler = MatchWrestler(
            match_id=db_match.id,
            wrestler_id=wrestler_entry.wrestler_id,
            is_winner=wrestler_entry.is_winner,
            team=wrestler_entry.team
        )

        db.add(match_wrestler)

    db.commit()
    return db_match

    
@router.get("/", response_model=List[MatchRead])
async def get_matches(
    skip: int = 0,
    limit: int = 100,
    match_type: Optional[MatchType] = None, 
    event_id: Optional[int] = None, 
    wrestler_id: Optional[int] = None,
    from_date: Optional[datetime] = None, 
    to_date: Optional[datetime] = None, 
    db: Session = Depends(get_db)
):
    
    query = select(Match)

    # Aplicamos los filtros
    if match_type:
        query = query.where(Match.match_type == match_type)
    if event_id:
        query = query.where(Match.event_id == event_id)
    if wrestler_id:
        query = query.join(MatchWrestler).where(MatchWrestler.c.wrestler_id == wrestler_id)
    if from_date:
        query = query.where(Match.match_date >= from_date)
    if to_date:
        query = query.where(Match.match_date <= to_date)

    # Ordenamos por fecha, más recientes primero
    query = query.order_by(Match.match_date.desc())

    statement = query.offset(skip).limit(limit)
    matches = db.exec(statement).all()

    return matches

@router.get("/{match_id}", response_model=MatchDetail)
async def get_match(match_id: int, db: Session = Depends(get_db)):
    print("siii")
    statement = select(Match).where(Match.id == match_id)
    match = db.exec(statement).first()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    # Obtener los luchadores de la lucha 
    wrestler_statement = select(MatchWrestler).where(MatchWrestler.match_id == match_id)
    wrestler_query = db.exec(wrestler_statement).all()

    wrestlers_data = []
    print(f"Los luchadores son: {wrestler_query}")
    for wrestler_entry in wrestler_query:
        wrestler_info = await get_wrestler_info(wrestler_entry.wrestler_id)
        if wrestler_info:
            wrestlers_data.append({
                "wrestler": wrestler_info,
                "is_winner": wrestler_entry.is_winner,
                "team": wrestler_entry.team
            })

    # Obtener información del evento
    event_info = await get_event_info(match.event_id)

    # Calcular el promedio de ratings 
    avg_rating_statement = select(func.avg(Rating.rating)).where(Rating.match_id == match_id)
    avg_rating = db.exec(avg_rating_statement).one_or_none() 
    avg_rating = avg_rating if avg_rating is not None else 0
    
    rating_count_statement = select(func.count(Rating.id)).where(Rating.match_id == match_id)
    rating_count = db.exec(rating_count_statement).one_or_none() 
    rating_count = rating_count if rating_count is not None else 0

    match_detail = {
        **match.model_dump(),
        "wrestlers": wrestlers_data,
        "event": event_info,
        "average_rating": round(float(avg_rating), 2),
        "rating_count": rating_count
    }

    return match_detail