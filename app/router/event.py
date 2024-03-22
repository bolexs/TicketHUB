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
