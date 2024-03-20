from app.model import Users
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

