from pydantic import BaseModel, HttpUrl


class SourceBase(BaseModel):
    title: str
    url: HttpUrl


class SourceCreate(SourceBase):
    pass


class SourceRead(SourceBase):
    id: int

    class Config:
        orm_mode = True
