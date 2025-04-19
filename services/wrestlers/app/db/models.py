from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, datetime, timezone
from sqlalchemy import Column, ForeignKey

class Wrestler(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    ring_name: str = Field(index=True, nullable=False)
    birth_date: Optional[date] = None 
    height: Optional[float] = None # cm 
    weight: Optional[float] = None # kg 
    from_city: Optional[str] = None 
    bio: Optional[str] = None 
    image_url: Optional[str] = None 
    active: bool = Field(default=True)
    debut_date: Optional[date] = None
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    stats: List["WrestlerStats"] = Relationship(back_populates="wrestler", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class WrestlerStats(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    wrestler_id: int = Field(sa_column=Column(ForeignKey("wrestler.id", ondelete="CASCADE"), nullable=False))
    wins: int = Field(default=0)
    losses: int = Field(default=0)
    draws: int = Field(default=0)
    championships: int = Field(default=0)
    average_match_rating: float = Field(default=0.0)
    total_matches: int = Field(default=0)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    wrestler: Wrestler = Relationship(back_populates="stats", sa_relationship_kwargs={"cascade": "all, delete"})