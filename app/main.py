
import time

import psycopg2
import snowflake.connector
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from .models import Base
from .database import engine
from .routers import auth, posts, users, votes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
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
# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection succesfull')
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("error: ", error)
#         time.sleep(2)




@app.get("/")
def root_message():
    
    return {"message":"Hello world"}    





