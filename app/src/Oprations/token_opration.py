def token_create(data: dict) :
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

