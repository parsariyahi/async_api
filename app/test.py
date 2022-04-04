from src import User_DB, Product_DB, db
import asyncio

product = Product_DB(db)


loop = asyncio.get_event_loop()
res = loop.run_until_complete(product.all_product())

print(res)