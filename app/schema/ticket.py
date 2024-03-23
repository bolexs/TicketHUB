from pydantic import validator, BaseModel
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    event_id: int
    user_id: int
    quantity: int

    @validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v

class TicketPurchase(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass

class TicketInDB(TicketBase):
    id: int
    purchase_date: datetime

    class Config:
        orm_mode = True