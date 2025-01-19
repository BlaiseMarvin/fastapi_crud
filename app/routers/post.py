from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import schemas,  utils, database
from ..schemas import PostCreate, Post
from .. import oauth2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier

db = database.DatabaseManager()
cursor = db.get_cursor()
conn = db.get_connection()

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/")
def get_posts():
    cursor.execute("""SELECT * FROM  post""")
    posts = cursor.fetchall()
    return {"data": posts}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # need to save your modifications to the database now
    conn.commit()
    return {"data": new_post}

@router.get("/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM post WHERE id = %s""",(id,))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"data": post}

# deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute(SQL("DELETE FROM {} WHERE id = %s RETURNING *").format(Identifier('post')),(id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update post
@router.put("/{id}")
def update_post(id: int, post: PostCreate, user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""UPDATE post SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *""",
                   (post.title, post.content,post.published,id,))
    conn.commit()
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    return {'data': updated_post}