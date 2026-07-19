import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ShortenRequest, ShortenResponse, URLStats
from app import crud

app = FastAPI(title="URL Shortener", version="1.0.0")

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse, status_code=201)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    try:
        url_obj = crud.create_short_url(
            db,
            original_url=str(payload.url),
            custom_code=payload.custom_code,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return ShortenResponse(
        short_code=url_obj.short_code,
        short_url=f"{BASE_URL}/{url_obj.short_code}",
        original_url=url_obj.original_url,
        created_at=url_obj.created_at,
    )


@app.get("/{code}/stats", response_model=URLStats)
def url_stats(code: str, db: Session = Depends(get_db)):
    url_obj = crud.get_stats(db, code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="Short code not found.")
    return url_obj


@app.get("/{code}")
def redirect_url(code: str, db: Session = Depends(get_db)):
    url_obj = crud.get_url_by_code(db, code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="Short code not found.")
    crud.increment_hit(db, url_obj)
    return RedirectResponse(url=url_obj.original_url, status_code=302)
