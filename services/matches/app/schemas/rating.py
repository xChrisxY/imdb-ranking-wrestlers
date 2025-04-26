from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime 

class RatingBase(BaseModel):
    match_id: int 
    rating: float  # 0-5 con decimalees
    comment: Optional[str] = None 

class RatingCreate(RatingBase):
    pass

class RatingUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None 

class RatingRead(RatingBase):
    id: int 
    user_id: int 
    created_at: datetime 
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = None 

class TopRatedMatch(BaseModel):
    id: int
    event_id: int
    match_type: str
    title_match: int
    duration: Optional[int] = None
    match_date: datetime
    description: Optional[str] = None
    main_event: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    average_rating: float
    rating_count: int
    event: Optional[Dict[str, Any]] = None
    wrestlers: List[Dict[str, Any]] = None 
    

