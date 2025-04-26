from pydantic import BaseModel 
from typing import List, Optional, Dict, Any 
from datetime import datetime 
from app.db.models import MatchType

class WrestlerEntry(BaseModel):
    wrestler_id: int
    is_winner: int = 0
    team: int = 0

class MatchBase(BaseModel):
    event_id: int 
    match_type: MatchType 
    title_match: int = 0
    duration: Optional[int] = None 
    match_date: datetime
    description: Optional[str] = None 
    main_event: int = 0

class MatchCreate(MatchBase):
    wrestlers: List[WrestlerEntry]

class MatchUpdate(BaseModel):
    
    event_id: Optional[int] = None 
    match_type: Optional[MatchType] = None
    title_match: Optional[int] = 0
    duration: Optional[int] = None 
    match_date: Optional[datetime] = None
    description: Optional[str] = None 
    main_event: Optional[int] = 0
    wrestlers: Optional[List[WrestlerEntry]] = None

class MatchRead(MatchBase):
    id: int 
    created_at: datetime 
    updated_at: Optional[datetime] = None 
    
    class Config:
        from_attributes = True 
        
class MatchDetail(MatchRead):
    wrestlers: List[Dict[str, Any]]
    event: Optional[Dict[str, Any]] = None
    average_rating: float = 0.0
    rating_count: int = 0


