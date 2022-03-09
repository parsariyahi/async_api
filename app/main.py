from lib2to3.pgen2 import token
from msilib import schema
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTERROR, jwt

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


class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    username : Optional[str] = None


class User(BaseModel):
    username : str
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email : Optional[str] = None
    national_id : Optional[int] = None


class UserInDB(User):
    password : str


scheme = OAuth2PasswordBearer(tokenUrl='token')


app = FastAPI()

# TODO hash passwords

def user_get(db, username : str) :
    if username in db :
        user = db['username']
        return UserInDB(**user)

def user_pass_check(password, user_password) :
    return password == user_password

def user_authenticate(db, username : str, password : str) :
    user = user_get(db, username)
    if user :
        if user_pass_check(password, user.password) :
            return True

    return None
    #return False

# TODO create expire time for token
def create_accsess_token(data : dict) :
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def user_current_get(token : str = Depends(schema)) :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try :
        user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = user.get('sub', None)
        if username :
            user = user_get(user_fake_db, username)
            if user :
                return user
        else :
            raise credentials_exception
    except JWTERROR :
        raise credentials_exception

@app.post('/token', response_model=Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends()) :
    user = user_authenticate(user_fake_db, form_data.username, form_data.password)

    if user :
        access_token = create_accsess_token({'sub' : user.username})
        return {'access_token' : access_token, 'token_type' : 'bearer'}

    # if user was not found return 401 error
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'incorrect username or password',
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get('/user/myinf/', response_model=Token)
async def user_info(current_user : User) :
    return user_current_get(current_user)