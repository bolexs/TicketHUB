from fastapi import (status, HTTPException,
                     Depends, APIRouter)
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.model import Event, Users, Ticket
from app.schema.event import (EventCreate, EventInDB,
                              EventResponse, EventUpdate)
from utils.auth import get_current_user
from app.schema.user import TokenData
from typing import List


router = APIRouter(tags=["Events"], prefix="/api/v1/events")

def get_session_local():
    yield SessionLocal()

@router.post('', status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, token_data: TokenData = Depends(get_current_user), db: Session = Depends(get_session_local)):
    user = db.query(Users).filter(Users.email == token_data.email).first()

    if user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can create events")

    event_dict = event_data.dict()
    event_dict.pop('organizer_id', None)
    event = Event(**event_dict, organizer=user)
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return {"message": "Event created successfully", "event": event}

@router.put('/{event_id}', response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate, token_data: TokenData = Depends(get_current_user), db: Session = Depends(get_session_local)):
    user = db.query(Users).filter(Users.email == token_data.email).first()

    if user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can update events")

    event_dict = event_data.dict(exclude_unset=True)
    event_dict.pop('organizer_id', None)

    event = db.query(Event).filter(Event.id == event_id).first()

    if event.organizer.email != user.email:
        raise HTTPException(status_code=403, detail="You are not authorized to update this event")
    
    for key, value in event_dict.items():
        setattr(event, key, value)

    db.query(Event).filter(Event.id == event_id).update(event_dict)
    db.commit()
    db.refresh(event)

    return {"message": "Event updated successfully", "event": event}

@router.get("/all-events", response_model=List[EventInDB])
def get_all_events(current_user: Users = Depends(get_current_user) ,db: Session = Depends(get_session_local)):
    events = db.query(Event).all()
    if not events:
        raise HTTPException(status_code=404, detail="No events found")
    
    return events

@router.get('/{event_id}', response_model=EventInDB)
def get_event(event_id: int, db: Session = Depends(get_session_local), current_user: TokenData = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    user = db.query(Users).filter(Users.email == current_user.email).first()
    user_tickets = db.query(Ticket).filter(Ticket.user_id == user.id).all()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if not (event.organizer.email == current_user.email or any(ticket.event_id == event_id for ticket in user_tickets)):
        raise HTTPException(status_code=403, detail="You are not authorized to view this event")

    return event

@router.delete('/{event_id}')
def delete_event(event_id: int, db: Session = Depends(get_session_local), current_user: TokenData = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.organizer.email != current_user.email:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this event")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}

@router.get("/organizer/{organizer_id}", response_model=List[EventInDB])
def get_events_by_organizer(organizer_id: int, db: Session = Depends(get_session_local), current_user: TokenData = Depends(get_current_user)):
    events = db.query(Event).filter(Event.organizer_id == organizer_id).all()

    for event in events:
        if event.organizer.email != current_user.email:
            raise HTTPException(status_code=403, detail="You are not authorized to view these events")

    if not events:
        raise HTTPException(status_code=404, detail="No events found for this organizer")

    return events
