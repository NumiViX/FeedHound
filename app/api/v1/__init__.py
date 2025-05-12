from fastapi import APIRouter

from app.api.v1 import source, news, auth, users

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth.router)
v1_router.include_router(users.router)
v1_router.include_router(source.router)
v1_router.include_router(news.router)
