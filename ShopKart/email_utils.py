from fastapi_mail import FastMail, MessageSchema
from fastapi import BackgroundTasks, HTTPException
from .config import conf
from .token import create_access_token  # Your JWT token generator

# When a user signs up:
# We generate a unique verification token.
# We send them an email with a link containing the token.
# When they click the link, they hit a FastAPI route that:
# reads the token
# validates it
# updates the user as "verified" in the database.

async def send_verification_email(email: str, user_id: int):
    token = create_access_token({"sub": str(user_id)})
    verify_link = f"http://localhost:8000/Users/verify-email?token={token}"
    message = MessageSchema(
    subject="Email Verification",           # Subject line
    recipients=[email],                     # Recipient list (must be a list)
    body=f"Hi, please click the link to verify your email: {verify_link}",  # Message content
    subtype="plain"                         # Content type ('plain' or 'html')
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Email failed to send")
    
async def send_password_verification_email(email: str):
    token = create_access_token({"sub": str(email)})
    verify_link = f"http://localhost:8000/Users/reset_password?token={token}"
    message = MessageSchema(
    subject="Email Verification to reset password",           # Subject line
    recipients=[email],                     # Recipient list (must be a list)
    body=f"Hi, please click the link to verify your email: {verify_link}",  # Message content
    subtype="plain"                         # Content type ('plain' or 'html')
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Email failed to send")



