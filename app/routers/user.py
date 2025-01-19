from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import schemas, utils, database
from ..schemas import PostCreate, Post
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier

db = database.DatabaseManager()
cursor = db.get_cursor()
conn = db.get_connection()

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate):
    # we need to hash the password first before it is actually stored - we cannot store actual password values
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""",(user.email, user.password))
    conn.commit()
    new_user = cursor.fetchone()
    return {"user": new_user}

@router.get("/", status_code=status.HTTP_200_OK)
def get_users():
    cursor.execute("""SELECT * FROM users""")
    users = cursor.fetchall()
    users = list(map(lambda x: {k:v for k,v in x.items() if k not in ['password','created_at']},users))
    return {"users": users}

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int):
    cursor.execute("""SELECT * FROM users WHERE id = %s""",(id,))
    user = cursor.fetchone()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} was not found")
    
    user = {k:v for k,v in user.items() if k not in ['password','created_at']}
    return {"user": user}