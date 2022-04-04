from typing import Optional
from re import match

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
import uvicorn

from .src import Token, TokenData, UserInDB, User, Product, User_DB, Product_DB, db

SECRET_KEY = 'de7cedf364a2bd8ace889a8179887ddbcbb474bcbb024dd782519f9b59e39d24'
ALGORITHM = 'HS256'

# --------------- database --------------- 
user_db = User_DB(db)
product_db = Product_DB(db)

scheme = OAuth2PasswordBearer(tokenUrl='token')
app = FastAPI()

# --------------- token functions  --------------- 
def token_create(data: dict) :
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# --------------- user functions  --------------- 
def user_is_exist(coll, username: str) -> bool :
    for user in coll.find(
        {'username': username},
        {'_id': 0},
    ) :
        if user :
            return True

    return False

def user_add(coll, user: UserInDB) -> bool :
    if user_is_exist(coll, user.username) :
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            'the user is exist',
        )
    coll.insert_one(user.dict())
    return True

def user_get(coll, username: str) -> UserInDB:
    for user in coll.find(
        {'username': username},
        {'_id': 0},
    ) :
        if user :
            return UserInDB(**user)

def user_password_check(password: str, user_password: str) -> bool :
    return password == user_password

def user_authenticate(coll, username: str, password: str) -> UserInDB :
    user = user_get(coll, username)
    if user :
        if user_password_check(password, user.password) :
            return user

async def user_current_get(token: str = Depends(scheme)) -> UserInDB :
    user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = user.get('sub')
    if username :
        user = user_get(user_coll, username)
        if user :
            return user

    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'invalid user',
    )

# --------------- validation  ---------------
def password_validation(password: str) -> None :
    """
    It contains at least 8 characters and at most 20 characters.
    It contains at least one digit (0-9)
    It contains at least one upper case alphabet (A-Z)
    It contains at least one lower case alphabet (a-z)
    It contains at least one special character which includes (! @ # $ % & * ( ) - + = ^ .)
    It does not contain any white space
    """
    if match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', password) :
        return None
    raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'invalid password',
            )

def email_validation(email: str) -> None :
    """
    the standard email format
    example@examle.xxx
    """
    if match(r'^[\w]+@([\w-]+\.)+[\w-]{2,4}$', email) :
        return None
    raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'invalid email',
            )

def national_id_validation(national_id: str) -> None :
    """
    it contains exactly ten digit
    iranian national id format is : xxx-xxxxxx-x
    """
    if len(national_id) == 10 :
        return None
    raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'invalid national id',
            )

def user_input_validation(password: str, email: str, national_id: str) -> bool :
    # here are all validator functions for user
    password_validation(password)
    email_validation(email)
    national_id_validation(national_id)
    return True


# --------------- product functions  --------------- 
def product_is_exist(coll, id: int) -> bool :
    for product in coll.find({'id': id}, {'_id': 0}) :
        if product :
            return True

    return False

def product_get(coll, id: int) -> Product :
    if product_is_exist(coll, id) :
        for product in coll.find({'id': id}, {'_id': 0}) :
            return Product(**product)

    raise HTTPException(
        status.HTTP_409_CONFLICT,
        'the product is not exist',
    )


def product_add(coll, product: Product) -> None:
    if product_is_exist(coll, product.id) :
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            'the product is exist',
        )
    try :
        coll.insert_one(product.dict())
    except :
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'Database error',
        )

def product_update(coll, id: int, key, value) -> Product :
    if product_is_exist(coll, id) :
        coll.update_one(
            {'id': id} ,
            {'$set': {key : value} },
        )
        return product_get(coll, id)

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        'the product is not exist',
    )

def product_delete(coll, id: int) -> bool :
    if product_is_exist(coll, id) :
        coll.delete_one({'id': id})
        return True

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        'the product is not exist',
    )


# --------------- routes ---------------
# this route will create the token
@app.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) :
    user = user_authenticate(user_coll, form_data.username, form_data.password)

    if user :
        access_token = token_create({'sub': user.username})
        return {'access_token': access_token}

    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'incorrect username or password',
    )


@app.post('/user/register/', status_code=status.HTTP_201_CREATED)
async def register(form_data: UserInDB) :
    if user_input_validation(
        form_data.password, \
        form_data.email, \
        form_data.national_id
    ) :  
        if user_add(user_coll, form_data) :
            {'detail': 'user created'}
    
# return aouthorized user info
@app.get('/user/myinf/', response_model=User)
async def user_info(current_user: User = Depends(user_current_get)) :
    return current_user

# CRUD -> create, read, update, delete
# read a prudoct whith id
@app.get('/product/read/{id}', response_model=Product)
async def get_product(id: int) :
    return product_get(product_coll, id)

# add new product
@app.post('/product/add/', status_code=status.HTTP_201_CREATED)
async def add_product(product: Product) :
    product_add(product_coll, product)

# update a product with id
@app.put('/product/edit/{id}', response_model=Product)
async def update_product(id: int, key, value) :
    return product_update(product_coll, id, key, value)

# delete a product with id
@app.delete('/product/del/{id}')
async def delete_product(id: int) :
    product_delete(product_coll, id)

# --------------- test routes ---------------
# test route for uesrs
@app.get('/user/all/')
async def user_all_get() :
    res = {}
    for user in user_coll.find({}, {'_id': 0}) :
        res[user['username']] = user

    return res

# test route for products
@app.get('/product/all/')
async def product_all_get() :
    res = {}
    for product in product_coll.find({}, {'_id': 0}) :
        res[product['id']] = product

    return res


if __name__ == '__main__' :
    uvicorn.run('main:app', debug=True)
