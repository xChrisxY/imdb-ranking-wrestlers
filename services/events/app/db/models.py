from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List 
from datetime import datetime, timezone
import enum

class EventType(str, enum.Enum):
    PPV = "ppv"
    SPECIAL = "special"
    NETWORK = "network"
    PREMIUM = "premium"

    
class ShowType(str, enum.Enum):
    RAW = "raw"
    SMACKDOWN = "smackdown"
    NXT = "nxt"
    MAIN_EVENT = "main_event"
    SUPERSTARS = "superstars"
    ECW = "ecw"
    WCW = "wcw"
    HEAT = "heat"
    VELOCITY = "velocity"
    THUNDER = "thunder"
    NITRO = "nitro"
    OTHER = "other"

class Venue(SQLModel, table=True):

    __tablename__: str = "venues"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=True)
    city: str = Field(nullable=True)
    state: Optional[str] = Field(default=None)
    country: str = Field(nullable=False)
    capacity: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    events: List["Event"] = Relationship(back_populates="venue")
    shows: List["Show"] = Relationship(back_populates="venue")

class Event(SQLModel, table=True):
    
    __tablename__: str = "events"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False, index=True)
    event_type: EventType = Field(nullable=False)
    date: datetime = Field(nullable=False) 
    venue_id: Optional[int] = Field(default=None, foreign_key="venues.id")
    description: Optional[str] = Field(default=None)
    attendance: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    venue: Optional["Venue"] = Relationship(back_populates="events")

class Show(SQLModel, table=True):
    
    __tablename__: str = "shows"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    show_type: ShowType = Field(nullable=False)
    episode_number: int = Field(default=None)
    date: datetime = Field(nullable=False)
    venue_id: Optional[int] = Field(default=None, foreign_key="venues.id")
    is_live: bool = Field(default=True)
    description: Optional[str] = Field(default=None)
    attendance: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    venue: Optional["Venue"] = Relationship(back_populates="shows")