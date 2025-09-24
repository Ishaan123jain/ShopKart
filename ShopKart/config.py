from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="2as1931042@gmail.com",
    MAIL_PASSWORD="gifn ypyx ownc iqrj", 
    MAIL_FROM="2as1931042@gmail.com",  
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="ShopKart",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
