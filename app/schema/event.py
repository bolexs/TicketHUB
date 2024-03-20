from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    name: str
    description: str
    date: datetime
    location: str
    price: float
    tickets: int
    organizer_id: int
    category_id: int

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventInDB(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
