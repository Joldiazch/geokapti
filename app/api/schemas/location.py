from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional


class LocationBase(SQLModel):
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class Location(LocationBase, table=True):
    id: int = Field(default=None, primary_key=True)
    added_on: datetime = Field(default_factory=datetime.utcnow)
    added_by: str = Field(default=None)
    changed_on: datetime = Field(default_factory=datetime.utcnow)
    changed_by: str = Field(default=None)
    user_id: int = Field(foreign_key="user.id")
    user: Optional['User'] = Relationship(back_populates="locations")
