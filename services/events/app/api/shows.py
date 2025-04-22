from fastapi import APIRouter, Depends, HTTPException, status, query
from sqlmodel import Session, select, desc
from typing import List, Optional
from datetime import datetime 

from app.db.models import Show, ShowType, Venue 
from app.db.session import get_db
from app.schemas.show import ShowCreate, ShowRead, ShowDetail, ShowUpdate

router = APIRouter() 

@router.post("/", response_model=ShowCreate, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowCreate, db: Session = Depends(get_db)):

    # verificamos que el venue si existe
    if show.venue_id:
        venue = db.get(Venue, show.venue_id)
        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )

    db_show = Show(**show.model_dump(exclude_unset=True))
    db.add(db_show)
    db.commit()
    db.refresh(db_show)

    return db_show

@router.get("/{show_id}", response_model=ShowDetail, status_code=status.HTTP_200_OK)
def get_show(show_id: int, db: Session = Depends(get_db)):
    
    show = db.get(Show, show_id)
    if not show:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Show not found"
        )
        
    venue = db.get(Venue, show.venue_id) if show.venue_id else None

    show_detail = ShowDetail(
        **show.model_dump(), 
        venue=venue.model_dump() if venue else None
    )
    
    return show_detail