from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
import random
import string
from datetime import datetime
from typing import List

from app.database import get_db
from app.models import URL
from app.schemas import CustomURLCreate, URLCreate, URLResponse, URLStats

router = APIRouter()

def generate_unique_code(db: Session, length: int = 6) -> str:
    while True:
        code = "".join(random.choices(string.ascii_letters + string.digits, k=length))
        if not db.query(URL).filter(URL.short_code == code).first():
            return code

@router.post("/shorten", response_model=dict)
def shorten_url(data: URLCreate, db: Session = Depends(get_db)):
    existing = db.query(URL).filter(URL.original_url == str(data.original_url)).first()
    if existing:
        return {"short_url": f"http://localhost:8000/api/{existing.short_code}"}

    code = generate_unique_code(db)
    url = URL(original_url=str(data.original_url), short_code=code)
    db.add(url)
    db.commit()
    db.refresh(url)
    return {"short_url": f"http://localhost:8000/api/{code}"}

@router.post("/custom", response_model=dict)
def custom_url(data: CustomURLCreate, db: Session = Depends(get_db)):
    existing_code = db.query(URL).filter(URL.short_code == data.custom_code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail="Code already exists")

    url = URL(original_url=str(data.original_url), short_code=data.custom_code)
    db.add(url)
    db.commit()
    return {"short_url": f"http://localhost:8000/api/{data.custom_code}"}

@router.get("/top", response_model=List[URLResponse])
def top_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).order_by(desc(URL.clicks)).limit(5).all()
    return urls

@router.get("/search", response_model=List[URLResponse])
def search(q: str, db: Session = Depends(get_db)):
    urls = db.query(URL).filter(URL.original_url.contains(q)).all()
    return urls

@router.get("/stats/{code}", response_model=URLStats)
def stats(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return URLStats(original_url=url.original_url, clicks=url.clicks)

@router.delete("/urls/{code}", response_model=dict)
def delete_url(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return {"message": "Deleted"}

@router.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    if url.expires_at and url.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="URL expired")
    url.clicks += 1
    db.commit()
    return RedirectResponse(url.original_url)