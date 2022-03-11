import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from typing import Optional
from re import match

SECRET_KEY = 'de7cedf364a2bd8ace889a8179887ddbcbb474bcbb024dd782519f9b59e39d24'

ALGORITHM = 'HS256'



# --------------- database --------------- 

user_fake_db = {
    'prrh' : {
        'username' : 'prrh',
        'first_name' : 'parsa',
        'last_name' : 'riyahi',
        'email' : 'parsa@gmail.com',
        'password' : 'parsa1234',
        'national_id' : '4619878165',
    }, 
    'alip' : {
        'username' : 'alip',
        'first_name' : 'ali',
        'last_name' : 'prkh',
        'email' : 'ali@gmail.com',
        'password' : 'ali1234',
        'national_id' : '0019878165',
    }, 
}


product_fake_db = {
    1 : {
        'id' : 1,
        'name' : 'ice cream',
        'price' : 5,
        'description' : 'a cold and sweet ice cream with choco',
        },

    2 : {
        'id' : 2,
        'name' : 'cream',
        'price' : 7,
        'description' : 'vanilla cream',
        },

    3 : {
        'id' : 3,
        'name' : 'milk',
        'price' : 10,
        'description' : 'its just white',
        },
}

# --------------- database --------------- 


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


class UserIn(User):
    password : str

class Product(BaseModel) :
    id : int
    name : str
    price : int
    description : Optional[str]

# --------------- models --------------- 


scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI()



# --------------- token functions  --------------- 

# TODO create expire time for token
def token_create(data : dict) :
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# --------------- token functions  --------------- 


# --------------- user functions  --------------- 

# TODO hash passwords
def user_get(db, username : str) :
    if username in db :
        user = db[username]
        return UserIn(**user)

def user_password_check(password : str, user_password : str) :
    return password == user_password

def user_authenticate(db, username : str, password : str) :
    user = user_get(db, username)
    if user :
        if user_password_check(password, user.password) :
            return user

    return None

def user_input_validation(password, email, national_id) :
    password_validation(password)
    email_validation(email)
    national_id_validation(national_id)

async def user_current_get(token : str = Depends(scheme)) :
    user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = user.get('sub')
    if username :
        user = user_get(user_fake_db, username)
        if user :
            return user

    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'invalid user'
    )

# --------------- user functions  --------------- 


def password_validation(password) :
    if match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', password) :
        return None

    raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'invalid password',
            )

def email_validation(email) :
    if match(r'^[\w]+@([\w-]+\.)+[\w-]{2,4}$', email) :
        return None
    else :
        raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'invalid email',
                )

def national_id_validation(national_id) :
    if len(national_id) == 10 :
        return None

    raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'invalid national id',
            )


# --------------- product functions  --------------- 

def product_get(db, id : int) -> Product : 
    if id in db :
        product = db[id]
        return Product(**product)

    return None
    #return False

def product_add(db, product: Product) :
    if product.id in db :
        return (None, 5)

    try :
        db[product.id] = {
                'id' : product.id,
                'name' : product.name,
                'price' : product.price,
                'description' : product.description,
        }

        return (product, 1)

    except :
        return (None, 0)

def product_update(db, id: int, key, value) :
    if id in db :
        db[id][key] = value
        return True

    return None

def product_delete(db, id: int) :
    if id in db :
        del db[id]
        return True

    return None

# --------------- product functions  --------------- 



@app.post('/token', response_model=Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends()) :
    user = user_authenticate(user_fake_db, form_data.username, form_data.password)

    if user :
        access_token = token_create({'sub' : user.username})
        return {'access_token' : access_token}

    # if user was not found return 401 error
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'incorrect username or password',
    )


@app.post('/user/register/')
async def register(form_data: UserIn) :
    user_input_validation(form_data.password, form_data.email, form_data.national_id)
    


# return aouthorized user info
@app.get('/user/myinf/', response_model=User)
async def user_info(current_user : User = Depends(user_current_get)) :
    return current_user

# read a prudoct whith id
@app.get('/product/read/{id}', response_model=Product)
async def get_product(id : int) :
    return product_get(product_fake_db, id)


# TODO create a better return with status codes
# add new product
@app.post('/product/add/', status_code=status.HTTP_201_CREATED)
async def add_product(product: Product) :
    res, status = product_add(product_fake_db, product)

    if res :
        return {'result' : res, 'db' : product_fake_db}

    if status == 5 :
        return {'result' : 'the product is alredy exist'}

    return {'result' : 'there is a problem! please try again'}

# update a product with id
@app.put('/product/edit/{id}')
async def update_product(id: int, key, value) :
    res = product_update(product_fake_db, id, key, value)
    
    if res :
        return {'result' : res, 'edited field' : product_fake_db[id]}
    
    return {'result' : False}

# delete a product with id
@app.delete('/product/del/{id}')
async def delete_product(id: int) :
    res = product_delete(product_fake_db, id)

    if res :
        return {'result' : res, 'deleted field' : product_fake_db}

    return {'result' : False}

if __name__ == '__main__' :
    uvicorn.run('main:app', debug=True)
