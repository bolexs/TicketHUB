from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    name: str
    description: str
    date: datetime
    location: str
    price: float
    ticket_count: int

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    price: Optional[float] = None
    ticket_count: Optional[int] = None

class EventInDB(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    organizer_id: int
    ticket_count: int

    class Config:
        orm_mode = True

class EventResponse(BaseModel):
    message: str
    event: EventInDB
