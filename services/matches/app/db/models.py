from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum

# Enum para los tipos de lucha
class MatchType(str, Enum):
    SINGLES = "singles"
    TAG_TEAM = "tag_team"
    TRIPLE_THREAT = "triple_threat"
    FATAL_FOUR_WAY = "fatal_four_way"
    BATTLE_ROYAL = "battle_royal"
    ROYAL_RUMBLE = "royal_rumble"
    LADDER = "ladder"
    TLC = "tlc"
    CAGE = "cage"
    HELL_IN_A_CELL = "hell_in_a_cell"
    ELIMINATION_CHAMBER = "elimination_chamber"
    IRON_MAN = "iron_man"
    STREET_FIGHT = "street_fight"
    LAST_MAN_STANDING = "last_man_standing"
    OTHER = "other"

class MatchWrestler(SQLModel, table=True):
    
    __tablename__: str = "match_wrestler"
    match_id: int = Field(foreign_key="matches.id", primary_key=True)
    wrestler_id: int = Field(primary_key=True)  # ID del luchador del servicio wrestlers
    is_winner: int = Field(default=0) 
    team: int = Field(default=0)

    
class Match(SQLModel, table=True):

    __tablename__: str = "matches"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(nullable=False) # ID del servicio de eventos
    match_type: MatchType = Field(nullable=False)
    title_match: int = Field(default=0) # 1 para si, 0 para no
    duration: Optional[int] = None # Duración en segundos
    match_date: datetime = Field(nullable=False)
    description: Optional[str] = None 
    main_event: int = Field(default=0)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    # Relaciones 
    ratings: List["Rating"] = Relationship(back_populates="match")
    wrestlers: List[MatchWrestler] = Relationship()


class Rating(SQLModel, table=True):

    __tablename__: str = "rating"
    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id", nullable=False)
    user_id: int = Field(nullable=False) # ID del usuario del servicio auth
    rating: float = Field(nullable=False) # 0-5 con decimales
    comment: Optional[str] = None 
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    match: Optional[Match] = Relationship(back_populates="ratings")