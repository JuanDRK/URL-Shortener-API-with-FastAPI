from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl

class CustomURLCreate(BaseModel):
    original_url: HttpUrl
    custom_code: str

class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class URLStats(BaseModel):
    original_url: str
    clicks: int

    class Config:
        from_attributes = True