from fastapi import APIRouter,Depends,HTTPException
from schemas import UserRequest,UserResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password,verify_password,create_access_token
from auth import get_current_user,require_admin
from fastapi.security import OAuth2PasswordRequestForm

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
def login(
    form_data:OAuth2PasswordRequestForm = Depends(),
    db:Session = Depends(get_db)):
    
    user_exists = db.query(User).filter(User.email == form_data.username).first()

    if not user_exists:
        raise HTTPException(
            status_code=404,
            detail="user doesn't exists")
    
    if not verify_password(form_data.password,
                           user_exists.password):
        raise HTTPException(
            status_code=401,
            detail="wrong password or email"
        )
    
    access_token = create_access_token(
        data= {"sub":user_exists.email,
               "role": user_exists.role}
    )
    

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
        
    
    
@router.get("/me",response_model=UserResponse)
def get_me(current:User = Depends(get_current_user)):
    return current


@router.get("/admin")
def admin_route(current_user : User = Depends(require_admin)):


    return { "message": f" welcome admin {current_user.username}"}

    


        
    
   



