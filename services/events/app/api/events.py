from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, desc
from typing import List, Optional
from datetime import datetime

from app.db.models import Venue, Event, EventType
from app.db.session import get_db
from app.schemas.event import EventCreate, EventRead, EventDetail, EventUpdate, VenueCreate, VenueRead

router = APIRouter()

@router.post("/venues/", response_model=VenueRead)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    
    db_venue = Venue(**venue.model_dump(exclude_unset=True))
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

@router.get("/venues/", response_model=List[VenueRead])
def get_venues(skip: int = 0, limit: int = 100, country: Optional[str] = None, db: Session = Depends(get_db)):

    query = select(Venue)
    if country:
        query = query.where(Venue.country == country)

    statement = query.offset(skip).limit(limit)
    venues = db.exec(statement).all()

    return [VenueRead.model_validate(venue) for venue in venues]

@router.get("/venues/{venue_id}", response_model=VenueRead)
def get_venue(venue_id: int , db: Session = Depends(get_db)): 
    
    venue = db.get(Venue, venue_id)
    
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )

    return VenueRead.model_validate(venue)


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    
    if event.venue_id:
        venue = db.get(Venue, event.venue_id)
        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )

    db_event = Event(**event.model_dump(exclude_unset=True))
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return EventRead.model_validate(db_event)

@router.get("/", response_model=List[EventRead], status_code=status.HTTP_200_OK)
def get_events(
    skip: int = 0, 
    limit: int = 0, 
    event_type: Optional[EventType] = None, 
    year: Optional[int] = None, 
    name: Optional[str] = None, 
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    
    query = select(Event)
    if event_type:
        query = query.where(Event.event_type == event_type)
    if year:
        query = query.where(db.func.year(Event.date) == year)
    if name:
        query = query.where(Event.name.ilike(f"%{name}%"))
    if from_date:
        query = query.where(Event.date >= from_date)
    if to_date:
        query = query.where(Event.date <= to_date)

    query = query.order_by(Event.date.desc())
    statement = query.offset(skip).limit(limit)
    events = db.exec(statement).all()

    return [EventRead.model_validate(event) for event in events]
    
@router.get("/{event_id}", response_model=EventDetail)
def get_event(event_id: int, db: Session = Depends(get_db)):
    
    statement = select(Event).where(Event.id == event_id)
    event = db.exec(statement).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Obtener información detallada, incluido el venue
    venue = None
    if event.venue_id:
        statement = select(Venue).where(Venue.id == event.venue_id)
        venue = db.exec(statement).first()

    # Creamos el objeto de respuesta 
    event_detail = {
        **event.__dict__,
        "venue": venue.__dict__ if venue else None 
    }
    
    return event_detail
    