from passlib.context import CryptContext

# password stuff defn
# we are telling passlib what hashing algorithm we wanna use
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)