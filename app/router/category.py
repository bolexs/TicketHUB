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

    if user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers are authorized to create categories")

    category_dict = category_data.dict()
    category_dict.pop('id', None)
    category = Category(**category_dict)

    db.add(category)
    db.commit()
    db.refresh(category)
    
    return {"message": "Category created successfully", "category": category}

@router.post('/{category_id}/events/{event_id}', status_code=status.HTTP_201_CREATED)
def associate_category_with_event(category_id: int, event_id: int, current_user: TokenData = Depends(get_current_user), db: Session = Depends(database.get_db)):
    user = db.query(Users).filter(Users.email == current_user.email).first()

    if user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers are authorized to associate categories with events")

    category = db.query(Category).get(category_id)
    event = db.query(Event).get(event_id)

    if not category or not event:
        raise HTTPException(status_code=404, detail="Category or Event not found")

    if event.organizer.email != current_user.email:
        raise HTTPException(status_code=403, detail="You are not authorized to associate this event with a category")

    category.events.append(event)

    db.commit()

    return {"message": "Event successfully associated with Category"}