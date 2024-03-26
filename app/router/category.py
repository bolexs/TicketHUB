from fastapi import (status, HTTPException,
                     Depends, APIRouter)
from sqlalchemy.orm import Session
from app import database
from app.model import Category, Event, Users
from app.schema.category import CategoryCreate, CategoryInDB, CategoryUpdate
from utils.auth import get_current_user
from app.schema.user import TokenData


router = APIRouter(tags=["Category"], prefix="/api/v1/category")


@router.post('', status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, token_data: TokenData = Depends(get_current_user), db: Session = Depends(database.get_db)):
    user = db.query(Users).filter(Users.email == token_data.email).first()
    event = db.query(Event).filter(Event.id == category_data.event_id).first()

    if user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers are authorized to create categories")

    category_dict = category_data.dict()
    category_dict.pop('id', None)
    category = Category(**category_dict, events=event)

    db.add(category)
    db.commit()
    db.refresh(category)
    
    return {"message": "Category created successfully", "category": category}