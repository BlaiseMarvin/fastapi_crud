from fastapi import APIRouter, status, HTTPException
from .. import database, schemas, utils, oauth2

db = database.DatabaseManager()
cursor = db.get_cursor()
conn = db.get_connection()

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials: schemas.UserLogin):
    cursor.execute("""SELECT id, email, password FROM users WHERE email = %s""",(user_credentials.email,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    # now check if the 2 passwords are the same - comparing the hashed password with the entered password which we also hash
    if not utils.verify(user_credentials.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )
    
    # if they have a valid email and password - we now create the token and return it
    access_token = oauth2.create_access_token(data={"user_id":user['id']})
    return {"access_token":access_token, "token_type": "bearer"}