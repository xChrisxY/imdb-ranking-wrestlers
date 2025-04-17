from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select 
from typing import List, Optional 

from app.db.session import get_db 
from app.db.models import Wrestler, WrestlerStats
from app.schemas.wrestler import WrestlerCreate, WrestlerRead, WrestlerWithStats

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

    return WrestlerRead.model_validate(new_wrestler)

    
@router.get("/", response_model=List[WrestlerRead])
def get_wrestlers(skip: int = 0, limit: int = 100, active: Optional[bool] = True, db: Session = Depends(get_db)):
    
    query = select(Wrestler)
    if active is not None:
        query = query.where(Wrestler.active == active)

    statement = query.offset(skip).limit(limit)
    wrestlers = db.exec(statement).all()

    return [WrestlerRead.model_validate(w) for w in wrestlers]