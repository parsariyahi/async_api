class User_DB :
    
    @staticmethod
    async def create_user(coll, user: dict) :
        await coll.insert_one(user)

    @staticmethod
    async def read_user(coll, username: str) :
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