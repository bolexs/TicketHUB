from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from app.schema import user
from app.utils import validator, services
from app import database
from typing import List
from app.utils.auth import get_current_user


router = APIRouter(tags=['Users'], prefix='/user')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(request: user.UserCreate, db: Session = Depends(database.get_db)):

    user = await validator.verify_email(request.email, db)

    if user:
        raise HTTPException(
            status_code=400,
            detail="This email is already registered on our system."
        )

    new_user = await services.new_user_register(request, db)

    return new_user