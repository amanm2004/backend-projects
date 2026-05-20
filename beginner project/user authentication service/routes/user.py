from fastapi import APIRouter,Depends,HTTPException
from schemas import UserRequest,UserLogin
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password,verify_password

router = APIRouter()


@router.post("/register")
def register(user:UserRequest,
             db:Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="email already exists"
        )
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created",
        "user_id": new_user.id
    }


@router.post("/login")
def login(user:UserLogin,db:Session = Depends(get_db)):
    
    user_exists = db.query(User).filter(User.email == user.email).first()

    if not user_exists:
        raise HTTPException(
            status_code=404,
            detail="user doesn't exists")
    
    if not verify_password(user.password,user_exists.password):
        raise HTTPException(
            status_code=401,
            detail="wrong password or email"
        )
    

    return {
        "message": "login successfull"
    }
        
    
    

        
    
   



