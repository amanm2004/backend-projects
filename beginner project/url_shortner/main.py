from fastapi import FastAPI
from pydantic import BaseModel
import random as rd
import string 
from fastapi.responses import RedirectResponse



app = FastAPI()

class UrlRequest(BaseModel):
    url : str


def url_generator():

    characters = string.ascii_letters + string.digits
    short_url = "".join(rd.choice(characters) for _ in range(6))
    return short_url
    


url_db = {}

@app.post("/send_url")
def url_shortener(req:UrlRequest):
    short_url = url_generator()
    url_db[short_url] = req.url
    print(url_db)

    return {
        "shortened Url":f"http:/127.0.0.1/{short_url}"
    }


@app.get("/{short_url}")
def get_url(url:str):
    full_url = url_db.get(url)
    if full_url:
        return RedirectResponse(full_url)
    
    return { 
        "url":"url not found"
    }
    




















@app.get("/health")
def health():
    return {"this server is running on 8000"}