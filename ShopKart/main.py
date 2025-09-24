from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .Routers import Products, Users, Cart


app = FastAPI()

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(Products.routers)

app.include_router(Users.routers)

app.include_router(Cart.routers)
