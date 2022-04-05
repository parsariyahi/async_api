from src import User_DB, Product_DB, db
import asyncio

#product = Product_DB(db)
#u_db = User_DB(db)

data = {
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "national_id": "string",
  "password": "string"
}

loop = asyncio.get_event_loop()
#res = loop.run_until_complete(u_db.create_user(data))
#print(res)
res = loop.run_until_complete(User_DB.read_user(db.users, 'parsarh'))
print(res)
