import random
import string

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import URL


CODE_CHARS = string.ascii_letters + string.digits
CODE_LENGTH = 8


def generate_code() -> str:
    return "".join(random.choices(CODE_CHARS, k=CODE_LENGTH))


def create_short_url(db: Session, original_url: str, custom_code: str | None = None) -> URL:
    code = custom_code or generate_code()
    # Retry on collision (unlikely but possible for random codes)
    for _ in range(5):
        url_obj = URL(short_code=code, original_url=original_url)
        db.add(url_obj)
        try:
            db.commit()
            db.refresh(url_obj)
            return url_obj
        except IntegrityError:
            db.rollback()
            if custom_code:
                raise ValueError(f"Short code '{custom_code}' is already taken.")
            code = generate_code()
    raise RuntimeError("Could not generate a unique short code after 5 attempts.")


def get_url_by_code(db: Session, code: str) -> URL | None:
    return db.query(URL).filter(URL.short_code == code).first()


def increment_hit(db: Session, url_obj: URL) -> None:
    url_obj.hit_count += 1
    db.commit()


def get_stats(db: Session, code: str) -> URL | None:
    return db.query(URL).filter(URL.short_code == code).first()
