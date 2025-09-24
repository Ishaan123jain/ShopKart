from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import func
from .. import schemas, models, OAuth, token
from ..Repository import UsersRepo
from sqlalchemy.orm import Session
from ..Database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from ..Hashing import Hash
from typing import List

routers = APIRouter(
    tags=['Users'],
    prefix='/Users'
)

@routers.post('/user_register')
def user_register(user : schemas.User,background_tasks: BackgroundTasks, db:Session = Depends(get_db)):
    return UsersRepo.UserRegistration(user, background_tasks, db)

@routers.get('/verify-email')
def user_verify(token: str, db:Session = Depends(get_db)):
    return UsersRepo.UserVerify(token, db)

@routers.post('/forget_password')
def forget_password(email: str, background_tasks: BackgroundTasks, db:Session = Depends(get_db)):
    return UsersRepo.ForgetPassword(email,background_tasks,db)

@routers.post('/reset_password')
def reset_password(new_password_form : schemas.ResetPasswordSchema, db:Session = Depends(get_db)):
    return UsersRepo.ResetPassword(new_password_form, db)

@routers.post('/user_login')
def user_login(user : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    print(f"Searching for user with email: {user.username}")
    
    # Case-insensitive email search and strip whitespace
    User = db.query(models.User).filter(func.lower(models.User.email) == func.lower(user.username.strip())).first()
    
    if not User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found, kindly register')
    
    if not Hash.verify(user.password, User.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect Password')

    print(f"received: {User.email}, {User.id}, {User.role}")

    access_token = token.create_access_token(data={"sub": User.email, "id": User.id, "role": User.role})
    return schemas.Token(access_token=access_token, token_type="bearer")


##OAuth2PasswordRequestForm = Depends()