from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from jose import JWTError, jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
 

SECRET_KEY = "mysecretkey"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password:str):

    return pwd_context.hash(password)




def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)




def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
        
    )

    return encoded_jwt

def verify_access_token(token:str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        role = payload.get("role")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        
        return {
                "email": email,
                "role": role
            }
    
    except:
        raise HTTPException(
            status_code=401,
            detail="toke is invalid or expired"
        )
    



def get_current_user(token:str = Depends(oauth2_scheme),
                     db:Session =Depends(get_db)):
    
    token_data= verify_access_token(token)
    email = token_data["email"]
    role = token_data["role"]

    user = db.query(User).filter(User.email == email).first()


    if user is None:
        raise HTTPException(
            status_code=401,
            detail="user not found"
        )
    

    return user






def require_admin(
        current_user: User = Depends(get_current_user)
):
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="admin only"
        )
    
    return current_user

    