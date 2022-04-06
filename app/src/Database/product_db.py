class Product_DB:

    @staticmethod
    async def create_product(coll, product: dict) :
        await coll.insert_one(product)

    @staticmethod
    async def delete_product(coll, id: int) :
        if await coll.delete_one(id) :
            return True

        return False

    @staticmethod
    async def read_product(coll, id: int) :
        res = await coll.find_one({'id': id}, {'_id': 0})
        if res :
            return res

        return False

    @staticmethod
    async def update_product(coll, id: int, key, val) :
        res = await coll.update_one({'id': id}, {'$set': {key: val}} )
        if res :
            return True
        return False

    @staticmethod
    async def all_product(coll) :
        res = []
        products = coll.find({}, {'_id': 0})
        if products :
            async for product in products:
                res.append(product)
            return res

        return False
