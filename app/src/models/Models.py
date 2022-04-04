from typing import Optional
from pydantic import BaseModel


# --------------- models --------------- 

class Token(BaseModel):
    access_token : str

class TokenData(BaseModel):
    username : Optional[str] = None


class User(BaseModel):
    username : str
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email : Optional[str] = None
    # national id should be string because sometimes it start with 0
    national_id : Optional[str] = None


class UserInDB(User):
    password : str

class Product(BaseModel) :
    id : int
    name : str
    price : int
    description : Optional[str]

