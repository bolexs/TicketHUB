from pydantic import BaseModel, EmailStr
from typing import Optional, List, Literal
from .event import EventBase


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Literal["attendee", "organizer"]


class DisplayUser(BaseModel):
    id: int
    name: str
    email: str
    role: str
class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    events: List[EventBase] = []
    tickets: List[str] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None