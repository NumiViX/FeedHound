from fastapi import FastAPI

from app.api.v1 import source, news

app = FastAPI()

app.include_router(source.router)
app.include_router(news.router)
