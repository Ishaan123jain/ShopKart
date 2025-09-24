from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    original_price = Column(Integer, nullable=False)
    product_image = Column(String)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow)

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    items = relationship('CartItem', back_populates='cart')

class CartItem(Base):
    __tablename__ = 'cartitems'
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey ('cart.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)
    # price = Column(Integer, nullable=False)

    product = relationship('Products')
    cart = relationship('Cart', back_populates='items')


