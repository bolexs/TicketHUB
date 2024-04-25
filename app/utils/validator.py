from typing import Optional
from sqlalchemy.orm import Session
from app.model import Users, Event


async def verify_email(email: str, db_session: Session) -> Optional[Users]:
    return db_session.query(Users).filter(Users.email == email).first()

async def verify_event_exist(event_id: int, db_session: Session) -> Optional[Event]:
    return db_session.query(Event).filter(Event.id == event_id).first()