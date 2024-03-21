from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database
from app.model import Users
from app.utils.auth import create_access_token


router = APIRouter(tags=['auth'])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm= Depends(), db: Session = Depends(database.get_db)):
    user = db.query(Users).filter(Users.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details='Invalid Credentials')


    
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
