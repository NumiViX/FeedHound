from datetime import datetime

from pydantic import BaseModel, HttpUrl


class NewsBase(BaseModel):
    title: str
    url: HttpUrl
    published_at: datetime


class NewsCreate(NewsBase):
    source_id: int


class NewsUpdate(BaseModel):
    title: str | None = None
    url: HttpUrl | None = None
    published_at: datetime | None = None
    source_id: int | None = None


class NewsRead(NewsBase):
    id: int
    source_id: int | None

    model_config = {
        "from_attributes": True
    }
