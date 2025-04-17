from sqlmodel import SQLModel, Field
from typing import Optional 
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(..., unique=True, index=True, nullable=False)
    username: str = Field(..., unique=True, index=True, nullable=False)
    password: str = Field(..., nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.now)})
