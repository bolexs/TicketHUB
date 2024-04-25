from app.model import Users, Event
from typing import List, Optional
from fastapi import HTTPException, status


async def new_user_register(request, db) -> Users:
    new_user = Users(name=request.name, email=request.email,
                     role=request.role, password=request.password)
    db.add(new_user)
    db.commit()

    return new_user


async def get_user_by_id(user_id, db) -> Optional[Users]:
    user_info = db.query(Users).get(user_id)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User credentials not found")
    return user_info


async def delete_user_by_id(user_id, db):
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()


async def new_event_register( db, event_data, user) -> List[Event]:
    event_dict = event_data.dict()
    event_dict.pop('organizer_id', None)
    event = Event(**event_dict, organizer=user)
    
    db.add(event)
    db.commit()
    db.refresh(event)

async def update_event_service(db, event_id, event_data, user) -> List[Event]:

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