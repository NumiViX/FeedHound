from pydantic import BaseModel, HttpUrl


class SourceBase(BaseModel):
    title: str
    url: HttpUrl


class SourceCreate(SourceBase):
    pass


class SourceRead(SourceBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class SourceUpdate(BaseModel):
    title: str | None
    url: HttpUrl | None
