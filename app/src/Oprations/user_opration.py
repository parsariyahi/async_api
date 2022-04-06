# --------------- user functions  --------------- 
def user_is_exist(coll, username: str) -> bool :
    for user in coll.find(
        {'username': username},
        {'_id': 0},
    ) :
        if user :
            return True

    return False

async def user_add(user: UserInDB) -> bool :
    #if user_is_exist(coll, user.username) :
    #    raise HTTPException(
    #        status.HTTP_409_CONFLICT,
    #        'the user is exist',
    #    )
    res = await User_DB.create_user(db.users, user.dict())
    if res:
        return True
    
    return False

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

