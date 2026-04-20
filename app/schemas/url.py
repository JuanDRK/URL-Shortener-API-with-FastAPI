from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl


class CustomURLCreate(BaseModel):
    original_url: HttpUrl
    custom_code: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Allowed chars: a-z, A-Z, 0-9, _ and -",
    )


class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime
    expires_at: Optional[datetime] = None


class URLStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    original_url: str
    clicks: int
