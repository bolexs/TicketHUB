from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from app.schema import user
from app.utils import validator, services
from app import database
from typing import List
from app.utils.auth import get_current_user


router = APIRouter(tags=['Users'], prefix='/api/v1/user')


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(request: user.UserCreate, db: Session = Depends(database.get_db)):

    user = await validator.verify_email(request.email, db)

    if user:
        raise HTTPException(
            status_code=400,
            detail="This email is already registered on our system."
        )

    new_user = await services.new_user_register(request, db)

    return {"message": "User created successfully", "user": new_user}



@router.get('/{user_id}', response_model=user.DisplayUser)
async def get_user_by_id(user_id: str, db: Session = Depends(database.get_db), current_user: user.UserBase = Depends(get_current_user)):
    return await services.get_user_by_id(user_id, db)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user(user_id: str, db: Session = Depends(database.get_db), current_user: user.UserBase = Depends(get_current_user)):
    return await services.delete_user_by_id(user_id, db)