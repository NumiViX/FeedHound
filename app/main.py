from fastapi import FastAPI

from app.api.v1 import source

app = FastAPI()

app.include_router(source.router, prefix="/sources", tags=["sources"])
