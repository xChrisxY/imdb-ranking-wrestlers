from pydantic import BaseModel
from typing import Optional, Dict, Any 
from datetime import date, datetime

class WrestlerBase(BaseModel):
    name: str 
    ring_name: str 
    birth_date: Optional[date] = None 
    height: Optional[float] = None # cm 
    weight: Optional[float] = None # kg 
    from_city: Optional[str] = None 
    bio: Optional[str] = None 
    image_url: Optional[str] = None 
    active: bool = True 
    debut_date: Optional[date] = None

class WrestlerCreate(WrestlerBase):
    pass

class WrestlerUpdate(BaseModel):
    name: Optional[str] = None
    ring_name: Optional[str] = None
    birth_date: Optional[date] = None 
    height: Optional[float] = None # cm 
    weight: Optional[float] = None # kg 
    from_city: Optional[str] = None 
    bio: Optional[str] = None 
    image_url: Optional[str] = None 
    active: Optional[bool] = True 
    debut_date: Optional[date] = None

class WrestlerRead(WrestlerBase):
    id: int 
    created_at: datetime
    updated_at: Optional[datetime] = None 
    
    class Config:
        from_attributes = True


class WrestlerStatsBase(BaseModel):
    wins: int = 0
    losses: int = 0
    draws: int = 0
    championships: int = 0
    average_match_rating: float = 0.0
    total_matches: int = 0

class WrestlerStats(WrestlerStatsBase):
    id: int 
    wrestler_id: int 
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 
        
class WrestlerWithStats(WrestlerRead):
    stats: Optional[WrestlerStats] = None