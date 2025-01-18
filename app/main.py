from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier
import time#
from dotenv import load_dotenv
import os

app = FastAPI()


# load the environment variables
load_dotenv(".env")

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# connect to the database
# putting connections in this try except block, just incase they fail
# while loop -> if we cannot connect to the database - we shouldn't access the rest of the api logic below, otherwise
# break out of it after we connect to the database
while True:
    
    try:
        conn = psycopg2.connect(host=os.getenv('HOST'), database=os.getenv('DATABASE'), user =os.getenv('USER'), password = os.getenv('PASSWORD'),
                                port=os.getenv('PORT'), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successful")
        break
    except Exception as error:
        print("Failed to connect to Database")
        print("Error: ", error)
        # prevents random and fast connection attempts
        time.sleep(2)

my_posts = [
    {"title": "title of post 1","content":"content of post 1","id": 1},
    {"title": "favourite foods", "content":"I like Pizza","id":2}
    ]


@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM  post""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # need to save your modifications to the database now
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM post WHERE id = %s""",(id,))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"data": post}

# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(SQL("DELETE FROM {} WHERE id = %s RETURNING *").format(Identifier('post')),(id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE post SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *""",
                   (post.title, post.content,post.published,id,))
    conn.commit()
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    return {'data': updated_post}
