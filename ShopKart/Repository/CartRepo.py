from fastapi import Depends, HTTPException, status
from .. import schemas, models, OAuth
from sqlalchemy.orm import Session, joinedload
from ..Database import get_db


def addCart_id(cartItem : schemas.cart, user: schemas.TokenData, db:Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user.user_id).first()
    if not cart:
        cart = models.Cart(user_id = user.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    item_present = db.query(models.CartItem).filter(models.CartItem.product_id == cartItem.id, models.CartItem.cart_id == cart.id).first()
    if item_present:
        item_present.quantity += cartItem.quantity
    else :
        new_cartitem = models.CartItem(cart_id = cart.id, product_id = cartItem.id, quantity = cartItem.quantity)
        db.add(new_cartitem)
    db.commit()
    # db.refresh(new_cartitem)
    return 'item added successfully'

def getCart(user: schemas.TokenData, db:Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user.user_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No cart available')
    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.cart_id == cart.id)
        .options(joinedload(models.CartItem.product))      
        #It eagerly loads the product relationship when querying CartItem (somewhat JOIN)
        .all()
    )

    return [
        schemas.getcart(
            product=item.product,
            quantity=item.quantity
        )
        for item in cart_items
    ]