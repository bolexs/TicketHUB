from fastapi import (status, HTTPException,
                     Depends, APIRouter)
from sqlalchemy.orm import Session
from app import database
from app.model import Ticket, Event, Users
from app.schema.ticket import TicketPurchase, TicketInDB
from utils.auth import get_current_user
from app.schema.user import TokenData
from typing import List


router = APIRouter(tags=["Tickets"], prefix="/api/v1/tickets")

@router.post("", status_code=status.HTTP_201_CREATED)
def buy_ticket(ticket_data: TicketPurchase, token_data: TokenData = Depends(get_current_user), db: Session = Depends(database.get_db)):
    user = db.query(Users).filter(Users.email == token_data.email).first()
    event = db.query(Event).filter(Event.id == ticket_data.event_id).first()

    if user.role != "attendee":
        raise HTTPException(status_code=401, detail="Kindly login to purchase tickets.")

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.ticket_count < ticket_data.quantity:
        raise HTTPException(status_code=400, detail="Tickets are sold out.")

    event.ticket_count -= ticket_data.quantity

    ticket = Ticket(event_id=ticket_data.event_id, user_id=user.id, quantity=ticket_data.quantity)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {"message": f"{ticket_data.quantity} Tickets purchased successfully.", "ticket_id": ticket.id}


@router.get('/attendee/{user_id}', response_model=List[TicketInDB])
def get_tickets(user_id: int, current_user: TokenData = Depends(get_current_user), db: Session = Depends(database.get_db)):
    user = db.query(Users).filter(Users.email == current_user.email).first()
    tickets = db.query(Ticket).filter(Ticket.user_id == user_id).all()

    if user.role != "attendee":
        raise HTTPException(status_code=401, detail="Only attendees are allowed to view tickets.")

    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found.")

    return tickets

@router.get('/{ticket_id}', response_model=TicketInDB)
def get_ticket(ticket_id: int, current_user: TokenData = Depends(get_current_user), db: Session = Depends(database.get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found. Contact organizer.")

    if ticket.attendee.email != current_user.email:
        raise HTTPException(status_code=403, detail="You are not authorized to view this ticket.")
    
    return ticket
