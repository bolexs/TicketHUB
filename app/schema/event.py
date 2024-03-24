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
    pass

class EventInDB(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    organizer_id: int
    ticket_count: int

    class Config:
        orm_mode = True
