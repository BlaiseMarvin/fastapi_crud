from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import timedelta
import datetime
import os
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv(".env")
# SECRET KEY
# ALGORITHM
# EXPIRATION TIME OF THE TOKEN

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

# these are 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = {"id": id}
    
    except JWTError:
        raise credentials_exception
    return token_data

# we now have this function below, which verifies that the access token is accurare and thereafter 
# extracts info from the payload
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)


