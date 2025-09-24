from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # import Base from your models.py

DATABASE_URL = 'postgresql://postgres:Ishaan123%40%23@localhost/ShopKart'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Import your models here to ensure they are registered with Base.metadata
  # This imports your models.py so tables are registered
#Base.metadata.drop_all(bind=engine)
# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
