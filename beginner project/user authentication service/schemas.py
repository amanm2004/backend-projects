from pydantic import BaseModel,EmailStr,field_validator
import re

class UserRequest(BaseModel):
    username:str
    email:EmailStr
    password:str


    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        #check length
        if len(value)<8:
            raise ValueError(
                "Password must be atleast 8 characters long"
            )
        
        #chech character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",value):
            raise ValueError(
                "Password must contain atleast one speacial character"
            )
        return value




class UserResponse(BaseModel):

    id: int
    username: str
    email: str
    role: str

    class Config:

        from_attributes = True
