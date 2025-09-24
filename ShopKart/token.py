from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from . import schemas, models
from sqlalchemy.orm import Session
from .Database import get_db


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception, db:Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email= payload.get("sub")
        user_id= payload.get("id")
        user_role= payload.get("role")
        if user_email is None:
            raise credentials_exception
        User = db.query(models.User).filter(models.User.id == user_id).first()
        if not User:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid User')
        if not User.is_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not verified')
        return schemas.TokenData(user_id= user_id, role=user_role)
    except JWTError:
        print(f'token.py me JWTError')
        raise credentials_exception
    
def verify_email_token(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id= payload.get("sub")
        if user_id is None:
            print(f'token.py me user_email me dikkat h')
            raise credentials_exception
        return schemas.TokenData(user_id= user_id)
    except JWTError:
        print(f'token.py me JWTError')
        raise credentials_exception
    
def reset_email_token(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email= payload.get("sub")
        if email is None:
            print(f'token.py me user_email me dikkat h')
            raise credentials_exception
        return email
    except JWTError:
        print(f'token.py me JWTError')
        raise credentials_exception



#  payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = payload.get("user_id")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return user_id
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")