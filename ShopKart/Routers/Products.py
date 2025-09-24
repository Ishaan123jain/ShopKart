from fastapi import APIRouter, Depends, UploadFile, Form, File
from .. import schemas, models, OAuth
from ..Repository import ProductsRepo
from sqlalchemy.orm import Session
from ..Database import get_db
from typing import List
import os, shutil

routers = APIRouter(
    tags=['Products'],
    prefix='/Products'
)

UPLOAD_FOLDER = "uploads/"
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@routers.post('/add_product')
#def add_product(Product : schemas.Product, db:Session = Depends(get_db), user: schemas.TokenData = Depends(OAuth.get_admin)):
def add_product(
    title: str = Form(...),
    category: str = Form(...),
    original_price: int = Form(...),
    product_image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    image_path = os.path.join(UPLOAD_FOLDER, product_image.filename)
    with open(image_path, 'wb') as f:
        shutil.copyfileobj(product_image.file, f)  #upload the file in chunks, unlike f.write
    return ProductsRepo.add_product(
        title=title,
        category=category,
        original_price=original_price,
        product_image=product_image.filename,
        db=db
    )

@routers.get('/get_products', response_model=List[schemas.Product])
def get_product(db:Session = Depends(get_db)):
    return ProductsRepo.getAll(db)

@routers.get('/get_product_by_id', response_model=schemas.Product)
def get_product_id(id, db:Session = Depends(get_db)):
    return ProductsRepo.getProduct_id(id, db)

@routers.get('/get_product_by_category', response_model=List[schemas.Product])
def get_product_category(category, db:Session = Depends(get_db)):
    return ProductsRepo.getProduct_category(category, db)

@routers.delete('/delete_product')
def delete_product(id, db:Session = Depends(get_db), user: schemas.TokenData = Depends(OAuth.get_admin)):
    return ProductsRepo.deleteProduct(id, db)

@routers.put('/update_product')
def update_product(id, response: schemas.Product, db:Session = Depends(get_db), user: schemas.TokenData = Depends(OAuth.get_admin)):
    return ProductsRepo.updateProduct(id,db)

