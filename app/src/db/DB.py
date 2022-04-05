class User_DB :

    @staticmethod
    async def create_user(coll, user: dict) :
        a = await coll.insert_one(user)
        return a

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
        users = coll.find()
        if users :
            async for user in users:
                res.append(user)
            return res

        return False

class Product_DB :
    def __init__(self, db) :
        self.db = db

    async def cereate_product(self, product: dict) :
        if await self.db.products.insert_one(product) :
            return True

        return False

    async def delete_product(self, id: int) :
        if await self.db.products.delete_one(id) :
            return True

        return False

    async def read_product(self, id: int) :
        res = await self.db.products.find_one({'id': id}, {'_id': 0})
        if res :
            return res

        return False

    async def update_product(self, id: int, key, val) :
        res = await self.db.products.update_one({'id': id}, {'$set': {key: val}} )
        if res :
            return True
        return False

    async def all_product(self) :
        res = []
        products = self.db.products.find()
        if products :
            async for product in products:
                res.append(product)
            return res

        return False
