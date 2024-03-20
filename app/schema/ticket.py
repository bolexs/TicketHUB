from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    event_id: int
    user_id: int

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass

class TicketInDB(TicketBase):
    id: int
    purchase_date: datetime

    class Config:
        orm_mode = True