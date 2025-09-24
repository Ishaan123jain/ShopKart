from fastapi import APIRouter, Depends
from .. import schemas, OAuth, models
from sqlalchemy.orm import Session
from ..Database import get_db
from typing import List
from ..Repository import CartRepo

routers = APIRouter(
    tags = ['Cart'],
    prefix = '/Cart'
)

@routers.post('/add_cart_by_id')
def addCart_id(cartItem : schemas.cart, user: schemas.TokenData = Depends(OAuth.get_current_user), db:Session = Depends(get_db)):
    return CartRepo.addCart_id(cartItem,user, db)

@routers.get('/get_cart', response_model=List[schemas.getcart])
def getCart(user: schemas.TokenData = Depends(OAuth.get_current_user), db:Session = Depends(get_db)):
    return CartRepo.getCart(user, db)