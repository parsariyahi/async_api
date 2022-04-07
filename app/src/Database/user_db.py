class User_DB :

    @staticmethod
    async def __is_user_exist(coll, username: str) :
        async for user in coll.find(
            {'username': username},
            {'_id': 0},
        ) :
            if user :
                return True
                
            return False

    @staticmethod
    async def __user_password_check(password: str, user_password: str) -> bool :
        return password == user_password

    @staticmethod
    async def __create_user(coll, user: dict) :
        await coll.insert_one(user)

    @staticmethod
    async def _read_user(coll, username: str) :
        """This funciton will read the user

        Inputs: [username: str]

        return: [user: dict] or [False]
        """
        user = await coll.find_one({'username': username}, {'_id': 0})
        if user :
            return user

        return False

    @staticmethod
    async def all_user(coll) :
        res = []
        users = coll.find({}, {'_id': 0})
        if users :
            async for user in users:
                res.append(user)
            return res

        return False


    @staticmethod
    async def user_authenticate(coll, username: str, password: str) :
        user = await User_DB._read_user(coll, username)
        if user :
            if await User_DB.__user_password_check(password, user['password']) :
                del user['password']
                return user
        
        return False

    @staticmethod
    async def register(coll, user: dict) :
        if await User_DB.__create_user(coll, user) :
            return True

        return False
