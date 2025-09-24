from fastapi import Depends, HTTPException, status
from .. import schemas, models, OAuth
from sqlalchemy.orm import Session
from ..Database import get_db


def add_product(title: str, category: str, original_price: int, product_image: str, db: Session):
    New = models.Products(title = title, category=category,original_price=original_price, product_image=product_image)
    db.add(New)
    db.commit()
    db.refresh(New)
    return 'Product added successfully'

def getAll(db : Session = Depends(get_db)):
    getAll = db.query(models.Products).all()
    return getAll

def getProduct_id(id, db : Session = Depends(get_db)):
    getProduct= db.query(models.Products).filter(models.Products.id == id).first()
    if not getProduct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product does not exist')
    return getProduct

def getProduct_category(category, db : Session = Depends(get_db)):
    getProduct= db.query(models.Products).filter(models.Products.category == category).all()
    if not getProduct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Category')
    return getProduct

def deleteProduct(id, db : Session = Depends(get_db)):
    db.query(models.Products).filter(models.Products.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Product is deleted'

def updateProduct(id, response: schemas.Product, db:Session = Depends(get_db)):
    getproduct = db.query(models.Products).filter(models.Products.id == id).first()
    if not getproduct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product does not exist')
    getproduct.title = response.title
    getproduct.category = response.category
    getproduct.original_price = response.original_price
    db.commit()
    return 'Product is updated'