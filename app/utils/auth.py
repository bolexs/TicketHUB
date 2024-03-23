from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schema import user
from app.conf.settings import settings
from app.model import Users

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = "HS256"


# create OAuth2PasswordBearer instance with token url as parameter in json
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") 

# create access token

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# decode and verify jwt token

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = user.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception =  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(data, credentials_exception)