from datetime import datetime
from pydantic import BaseModel, HttpUrl, field_serializer


class ShortenRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = None


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: datetime

    model_config = {"from_attributes": True}


class URLStats(BaseModel):
    short_code: str
    original_url: str
    created_at: datetime
    hit_count: int

    model_config = {"from_attributes": True}
