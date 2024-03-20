from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.model import UserRole
from .event import EventBase


class UserRole(BaseModel):
    attendee = "attendee"
    organizer = "organizer"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

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