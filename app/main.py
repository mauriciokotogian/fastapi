
import time
from datetime import date, datetime

import psycopg2
import snowflake.connector
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import auth, posts, users, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print('Database connection succesfull')
        break
    except Exception as error:
        print("Connection to database failed")
        print("error: ", error)
        time.sleep(2)


ctx = snowflake.connector.connect(
    user='WS2_DEV_USER_API_DREAMFACTORY',
    password='dreamfactory',
    account='jza84063.us-east-1'
    )
cs = ctx.cursor()


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


@app.get("/feodo")
async def test_feodo(
    from_date : date | None = None, q : str = None):
   # try:
        today = datetime.today()
        print(from_date)
        print(today)
        return "hello"
        
       # thirty_days_ago = today - timedelta(days=30)
       # format_date = "'"+from_date+"'"
       # print(format_date)
        #print("SELECT * from ingest_db_dev.feodo.ip_blocklist where ingest_ts > "+ format_date)
        #cs.execute("SELECT data, ingest_ts from ingest_db_dev.feodo.ip_blocklist where ingest_ts > %s",(from_date))
        #print("query executed")
     
        #all_rows = cs.fetchall()
        #print(len(all_rows))


      #  cs.execute(" SELECT * from ingest_db_dev.feodo.ip_blocklist where ingest_ts > '2022-10-10'")

     #   all_rows = cs.fetchall()
      #  print(len(all_rows))

       # query = " SELECT * from ingest_db_dev.feodo.ip_blocklist where ingest_ts > "+format_date
       # print("query "+query)

     #   cs.execute(query)
      #  all_rows = cs.fetchall()
      #  print(len(all_rows))

     #   print(len(all_rows))
      #  cs.execute_async
        #print(len(one_row))
        #print(one_row[0])

        #async execute
        
   # finally:
    #    cs.close()

    #ctx.close()
       





