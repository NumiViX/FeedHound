from fastapi import APIRouter

from app.api.v1 import source, news, auth

main_router = APIRouter()

main_router.include_router(auth.router)
main_router.include_router(source.router)
main_router.include_router(news.router)
