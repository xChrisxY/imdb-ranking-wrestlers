from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.db.models import EventType

class VenueBase(BaseModel):
    name: str
    city: str 
    state: Optional[str] = None 
    country: str = "EEUU"
    capacity:Optional[int] = None

class VenueCreate(VenueBase):
    pass

class VenueRead(VenueBase):
    id: int 
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EventBase(BaseModel):

    name: str 
    event_type: EventType
    date: datetime 
    venue_id: Optional[int] = None
    description: Optional[str] = None
    attendance: Optional[str] = None
    image_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    
    name: Optional[str] = None
    event_type: Optional[EventType] = None
    date: Optional[datetime] = None
    venue_id: Optional[int] = None
    description: Optional[str] = None
    attendance: Optional[str] = None
    image_url: Optional[str] = None

class EventRead(EventBase):
    
    id: int 
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EventDetail(EventRead):
    venue: Optional[VenueRead] = None