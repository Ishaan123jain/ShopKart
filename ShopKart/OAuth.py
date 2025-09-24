from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .Database import get_db
from . import token
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Users/user_login")

def get_current_user( data: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(data, credentials_exception, db)

def get_admin(current_user: schemas.TokenData = Depends(get_current_user)):
    if current_user.role.lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only Admin can access')
    return current_user