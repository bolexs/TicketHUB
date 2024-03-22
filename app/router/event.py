from fastapi import (status, HTTPException,
                     Depends, APIRouter)
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.model import Event, Users
from app.schema.event import EventCreate
from utils.auth import get_current_user
from app.schema.user import TokenData

router = APIRouter(tags=["Events"])

def get_session_local():
    yield SessionLocal()

@router.post("/events/", status_code=status.HTTP_201_CREATED)
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

@router.put('/events/{event_id}')
def update_event(event_id: int, event_data: EventCreate, token_data: TokenData = Depends(get_current_user), db: Session = Depends(get_session_local)):
    user = db.query(Users).filter(Users.email == token_data.email).first()

    if user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can update events")

    event_dict = event_data.dict()
    event_dict.pop('organizer_id', None)

    event = db.query(Event).filter(Event.id == event_id).first()

    db.query(Event).filter(Event.id == event_id).update(event_dict)
    db.commit()
    db.refresh(event)

    return {"message": "Event updated successfully"}

@router.get('/events/{event_id}')
def get_event(event_id: int, db: Session = Depends(get_session_local)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
