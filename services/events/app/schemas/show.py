from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.db.models import ShowType

class ShowBase(BaseModel):
    show_type: ShowType
    episode_number: Optional[int] = None
    date: datetime 
    venue_id: Optional[int] = None
    is_live: bool = True
    description: Optional[str] = None
    attendance: Optional[int] = None

class ShowCreate(ShowBase):
    pass

class ShowUpdate(BaseModel):
    show_type: Optional[ShowType] = None
    episode_number: Optional[int] = None
    date: Optional[datetime] = None
    venue_id: Optional[int] = None
    is_live: Optional[bool] = True
    description: Optional[str] = None
    attendance: Optional[int] = None

class ShowRead(ShowBase):
    
    id: int 
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

        
class ShowDetail(ShowRead):
    venue: Optional[Dict[str, Any]] = None