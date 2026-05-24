from fastapi import FastAPI,Depends
from routes.user import router as user_router
from database import engine,Base


Base.metadata.create_all(bind=engine)


app = FastAPI()



@app.get("/")
def home():
    return {"server is running on port 8000"}


app.include_router(user_router)

