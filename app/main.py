from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt

SECRET_KEY = 'de7cedf364a2bd8ace889a8179887ddbcbb474bcbb024dd782519f9b59e39d24'
ALGORITHM = 'HS256'

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
        'price' : 1,
        'description' : 'vanilla cream',
        },

    3 : {
        'id' : 3,
        'name' : 'milk',
        'price' : 10,
        'description' : 'its just white',
        },
}


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


scheme = OAuth2PasswordBearer(tokenUrl='token')


app = FastAPI()

# TODO hash passwords
def user_get(db, username : str) :
    if username in db :
        user = db[username]
        return UserIn(**user)

def user_pass_check(password : str, user_password : str) :
    return password == user_password

def user_authenticate(db, username : str, password : str) :
    user = user_get(db, username)
    if user :
        if user_pass_check(password, user.password) :
            return user

    return None
    #return False

# TODO create expire time for token
def create_accsess_token(data : dict) :
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def user_current_get(token : str = Depends(scheme)) :
    user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = user.get('sub')
    if username :
        user = user_get(user_fake_db, username)
        if user :
            return user

@app.post('/token', response_model=Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends()) :
    user = user_authenticate(user_fake_db, form_data.username, form_data.password)

    if user :
        access_token = create_accsess_token({'sub' : user.username})
        return {'access_token' : access_token}

    # if user was not found return 401 error
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'incorrect username or password',
    )


@app.get('/user/myinf/', response_model=User)
async def user_info(current_user : User = Depends(user_current_get)) :
    return current_user
