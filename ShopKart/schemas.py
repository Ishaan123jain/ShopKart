from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class Product(BaseModel):
    id :int
    title : str
    category : str
    original_price : int
    product_image : str

    class Config():
        from_attributes = True

class User(BaseModel):
    name : str
    email : str
    password : str
    role : str
    class Config():
        from_attributes = True

class userLogin(BaseModel):
    email : str
    password : str
    class Config():
        from_attributes = True

class cart(BaseModel):
    id: int
    quantity : int

class getcart(BaseModel):
    product : Product
    quantity : int
    class Config():
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenDataVerify(BaseModel):
    user_id: int
    class Config():
        from_attributes = True

class TokenData(BaseModel):
    user_id: int
    role: Optional[str] = None
    class Config():
        from_attributes = True

class passwordEmail(BaseModel):
    email: str
    class Config():
        from_attributes = True

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str