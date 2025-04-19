from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select 
from typing import List, Optional 

from app.db.session import get_db 
from app.db.models import Wrestler, WrestlerStats
from app.schemas.wrestler import WrestlerCreate, WrestlerRead, WrestlerWithStats, WrestlerUpdate

router = APIRouter()

@router.post("/", response_model=WrestlerRead)
def create_wrestler(wrestler: WrestlerCreate, db: Session = Depends(get_db)):
    
    # Validamos la existencia
    statement = select(Wrestler).where(Wrestler.ring_name == wrestler.ring_name)
    existing_wrestler = db.exec(statement).first()
    if existing_wrestler:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrestler with this ring name already exists."
        )

    # Creamos el luchador
    new_wrestler = Wrestler(**wrestler.model_dump(exclude_unset=True))
    db.add(new_wrestler)
    db.commit()
    db.refresh(new_wrestler)

    # Creamos las estádisticas iniciales 
    stats = WrestlerStats(wrestler_id=new_wrestler.id)
    db.add(stats)
    db.commit()

    return new_wrestler

    
@router.get("/", response_model=List[WrestlerRead])
def get_wrestlers(skip: int = 0, limit: int = 100, active: Optional[bool] = True, db: Session = Depends(get_db)):
    
    query = select(Wrestler)
    if active is not None:
        query = query.where(Wrestler.active == active)

    statement = query.offset(skip).limit(limit)
    wrestlers = db.exec(statement).all()

    return [WrestlerRead.model_validate(w) for w in wrestlers]


@router.get("/{wrestler_id}", response_model=WrestlerWithStats)
def get_wrestler(wrestler_id: int, db: Session = Depends(get_db)):
    
    wrestler = db.get(Wrestler, wrestler_id)
    if not wrestler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrestler not found"
        )

    statement = select(WrestlerStats).where(WrestlerStats.wrestler_id == wrestler_id)
    stats = db.exec(statement).first()

    return WrestlerWithStats.model_validate({**wrestler.model_dump(), "stats": stats.model_dump() if stats else None})

@router.put("/{wrestler_id}", response_model=WrestlerRead)
def update_wrestler(wrestler_id: int, wrestler_update: WrestlerUpdate, db: Session = Depends(get_db)):
    
    db_wrestler = db.get(Wrestler, wrestler_id)
    if not db_wrestler:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrestler not found")

    # Actualizamos solo los campos proporcionados
    wrestler_data = wrestler_update.model_dump(exclude_unset=True)
    for key, value in wrestler_data.items():
        setattr(db_wrestler, key, value)

    db.commit()
    db.refresh(db_wrestler)
    return WrestlerRead.model_validate(db_wrestler)

@router.delete("/{wrestler_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wrestler(wrestler_id: int, db: Session = Depends(get_db)):

    db_wrestler = db.get(Wrestler, wrestler_id)

    if not db_wrestler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrestler not found"
        )

    db.delete(db_wrestler)
    db.commit()

    return None