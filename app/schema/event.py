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
    organizer_id: Optional[int] = None
    category_id: Optional[int] = 0

class EventUpdate(EventBase):
    pass

class EventInDB(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
