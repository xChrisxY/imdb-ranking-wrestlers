from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get("/", response_model=List[ShowRead])
def get_shows(
    skip: int = 0,
    limit: int = 100,
    show_type: Optional[ShowType] = None,
    year: Optional[int] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    is_live: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = select(Show)

    if show_type:
        query = query.where(Show.show_type == show_type)
    if year:
        query = query.where(Show.date.year == year)
    if from_date:
        query = query.where(Show.date >= from_date)
    if to_date:
        query = query.where(Show.date <= to_date)
    if is_live is not None:
        query = query.where(Show.is_live == is_live)

    # Ordenamos por fecha, más recientes primero
    query = query.order_by(Show.date.desc())
    statement = query.offset(skip).limit(limit)
    shows = db.exec(statement).all()

    return [ShowRead.model_validate(s) for s in shows]


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


@router.put("/{show_id}", response_model=ShowRead, status_code=status.HTTP_200_OK)
def update_show(show_id: int, show_update: ShowUpdate, db: Session = Depends(get_db)):

    db_show = db.get(Show, show_id)
    if not db_show:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Show not found"
        )

    # Verificamos que el venue existe si se proporciona 
    if show_update.venue_id:
        venue = db.get(Venue, show_update.venue_id)
        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )

    # Actualizamos los campos del show
    for key, value in show_update.model_dump(exclude_unset=True).items():
        setattr(db_show, key, value)

    db.commit()
    db.refresh(db_show)
    return db_show

    
@router.delete("/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_show(show_id: int, db: Session = Depends(get_db)):

    db_show = db.get(Show, show_id)
    if not db_show:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Show not found"
        )

    db.delete(db_show)
    db.commit()
    return None
    
        
            
    