from fastapi import Depends, HTTPException, status, BackgroundTasks
from .. import schemas, models, token
from ..Hashing import Hash
from ..email_utils import send_verification_email, send_password_verification_email
from ..token import verify_email_token, reset_email_token
from sqlalchemy.orm import Session
from ..Database import get_db

def UserRegistration(user : schemas.User, background_tasks: BackgroundTasks, db:Session):
    User = db.query(models.User).filter(models.User.email==user.email).first()
    if User:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail='User already exist')
    
    User_new = models.User(name = user.name, password=Hash.hashpassword(user.password), email=user.email, role=user.role)
    db.add(User_new)
    db.commit()
    db.refresh(User_new)

    background_tasks.add_task(send_verification_email, user.email, User_new.id)

    return 'Kindly click on the verification link sent on your email for registration'

def UserVerify(token: str, db:Session):
    user_id = verify_email_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid User')
    User = db.query(models.User).filter(models.User.id == int(user_id.user_id)).first()
    if not User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    User.is_verified = True
    db.commit()
    db.refresh(User)
    return (f'Hi {User.name}, you are registered successfully. Kindly login and enjoy shopping!')

def ForgetPassword(email:str, background_tasks: BackgroundTasks, db:Session):
    User = db.query(models.User).filter(models.User.email == email).first()
    if not User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    background_tasks.add_task(send_password_verification_email, User.email)
    return 'Kindly click on the verification link sent on your email for verification'

def ResetPassword(new_password_form: schemas.ResetPasswordSchema, db:Session):
    email = reset_email_token(new_password_form.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sometihing went wrong!')
    User = db.query(models.User).filter(models.User.email == email).first()
    User.password = Hash.hashpassword(new_password_form.new_password)
    db.commit()
    db.commit()
    db.refresh(User)
    return 'password reset successfully'