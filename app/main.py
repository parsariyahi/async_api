from typing import Optional
from re import match

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient

from src import (
    Token, TokenData, UserInDB, User,
    Product, User_DB, Product_DB
    )

SECRET_KEY = 'de7cedf364a2bd8ace889a8179887ddbcbb474bcbb024dd782519f9b59e39d24'
ALGORITHM = 'HS256'

client = AsyncIOMotorClient('localhost', 27017)
db = client.simple_api_db
user_coll = db.users
product_coll = db.products

scheme = OAuth2PasswordBearer(tokenUrl='token')
app = FastAPI()




# --------------- routes ---------------
@app.get('/')
async def index():
    res = await User_DB.all_user(user_coll)
    return {'res': res}




# this route will create the token
# @app.post('/token', response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()) :
#     user = user_authenticate(user_coll, form_data.username, form_data.password)

#     if user :
#         access_token = token_create({'sub': user.username})
#         return {'access_token': access_token}

#     raise HTTPException(
#         status.HTTP_401_UNAUTHORIZED,
#         'incorrect username or password',
#     )


@app.post('/user/register/', status_code=status.HTTP_201_CREATED)
async def register(form_data: UserInDB) :
    #if user_input_validation(
        #form_data.password, \
        #form_data.email, \
        #form_data.national_id
    #) :  

    await User_DB.create_user(coll, form_data.dict())

    return {'res' : 'ksdjflkadjsfksadf'}

# return aouthorized user info
# @app.get('/user/myinf/', response_model=User)
# async def user_info(current_user: User = Depends(user_current_get)) :
#     return current_user








# CRUD -> create, read, update, delete
# read a prudoct whith id
@app.get('/product/read/{id}')
async def get_product(id: int) :
    res = await Product_DB.read_product(product_coll, id)
    return {'res': res}


# add new product
@app.post('/product/add/', status_code=status.HTTP_201_CREATED)
async def add_product(product: Product) :
    await Product_DB.create_product(product_coll, product.dict())

# update a product with id
# @app.put('/product/edit/{id}', response_model=Product)
# async def update_product(id: int, key, value) :
#     return product_update(product_coll, id, key, value)

# # delete a product with id
# @app.delete('/product/del/{id}')
# async def delete_product(id: int) :
#     product_delete(product_coll, id)

# --------------- test routes ---------------

# test route for products
@app.get('/product/all/')
async def product_all_get() :
    res = await Product_DB.all_product(product_coll)
    return {'res': res}


if __name__ == '__main__' :
    uvicorn.run('main:app', debug=True)
