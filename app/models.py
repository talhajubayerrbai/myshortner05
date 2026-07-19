from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(16), unique=True, index=True, nullable=False)
    original_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    hit_count = Column(BigInteger, default=0, nullable=False)
