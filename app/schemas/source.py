from pydantic import BaseModel, field_validator, HttpUrl


class SourceBase(BaseModel):
    title: str
    url: HttpUrl
    rss_url: HttpUrl

    model_config = {
        "json_encoders": {
            HttpUrl: lambda value: str(value)
        }
    }

    @field_validator("url", "rss_url", mode="after")
    @classmethod
    def convert_httpurl(cls, value):
        return str(value) if value else value


class SourceCreate(SourceBase):
    pass


class SourceRead(SourceBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class SourceUpdate(BaseModel):
    title: str | None = None
    url: HttpUrl | None = None
    rss_url: HttpUrl | None = None

    @field_validator("url", "rss_url", mode="after")
    @classmethod
    def convert_httpurl(cls, value):
        return str(value) if value else value
