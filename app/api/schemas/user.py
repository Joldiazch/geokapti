from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from typing import List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    locations: List['Location'] = Relationship(back_populates="user")
