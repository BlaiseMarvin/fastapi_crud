from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier
import time
from dotenv import load_dotenv
import os
from .schemas import PostCreate, Post
from . import schemas, utils
from .routers import post, user, auth


app = FastAPI()


# load the environment variables




# connect to the database
# putting connections in this try except block, just incase they fail
# while loop -> if we cannot connect to the database - we shouldn't access the rest of the api logic below, otherwise
# break out of it after we connect to the database
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Hello World"}