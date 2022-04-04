class User_DB :
    def __init__(self, db) :
        self.db = db

    async def create_user(self, user: dict) :
        if await self.db.users.insert_one(user) :
            return True

        return False

    async def read_user(self, username: str) :
        user = await self.db.users.find_one({'username': username}, {'_id': 0})
        if user :
            return user

        return False

    async def all_user(self) :
        res = []
        users = self.db.users.find()
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
