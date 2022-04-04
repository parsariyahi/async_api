import motor.motor_asyncio

from .models.Models import Token, TokenData, User, UserInDB, Product
from .db.DB import User_DB, Product_DB


# db connection for importing to the main.py
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.simple_api_db

