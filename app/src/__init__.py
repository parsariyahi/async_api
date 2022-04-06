from .Models.model import Token, TokenData, User, UserInDB, Product

from .Database.product_db import Product_DB
from .Database.user_db import User_DB

# db connection for importing to the main.py
# client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
# db = client.simple_api_db

