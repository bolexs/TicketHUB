from typing import Optional
from sqlalchemy.orm import Session
from app.model import Users


async def verify_email(email: str, db_session: Session) -> Optional[Users]:
    return db_session.query(Users).filter(Users.email == email).first()