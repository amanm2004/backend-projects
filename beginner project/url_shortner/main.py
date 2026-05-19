from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl

from database import SessionLocal, engine, Base
from models import URL
from utils import generate_short_code

app = FastAPI()

# Create tables automatically
Base.metadata.create_all(bind=engine)


# Request body model
class URLRequest(BaseModel):
    url: HttpUrl


# Database session dependency
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "URL Shortener Running"
    }


@app.post("/shorten")
def shorten_url(
    req: URLRequest,
    db: Session = Depends(get_db)
):

    # collision handling
    while True:

        short_code = generate_short_code()

        existing_url = db.query(URL).filter(
            URL.short_code == short_code
        ).first()

        if not existing_url:
            break

    # create ORM object
    new_url = URL(
        short_code=short_code,
        original_url=str(req.url)
    )

    # save to DB
    db.add(new_url)

    db.commit()

    return {
        "short_url": f"http://127.0.0.1:8000/{short_code}"
    }


@app.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):

    # find matching URL
    url_entry = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url_entry:

        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(url_entry.original_url)