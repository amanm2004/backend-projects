from sqlalchemy import Column,String,Integer
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    username = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    role = Column(String,default="user")