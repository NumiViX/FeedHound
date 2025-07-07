from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.session import get_async_session
from app.crud.news import news_crud
from app.schemas.news import NewsCreate, NewsRead, NewsUpdate

router = APIRouter(prefix="/news", tags=["News"])

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[NewsRead])
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    logger.debug("Fetching all news")
    return await news_crud.get_all(session)


@router.get("/{news_id}", response_model=NewsRead)
async def get_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    news = await news_crud.get_by_id(news_id, session)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    logger.debug("Returning news %s", news_id)
    return news


@router.post("/", response_model=NewsRead, status_code=201)
async def create_news(
    news: NewsCreate,
    session: AsyncSession = Depends(get_async_session)
):
    logger.info("Creating news %s", news.url)
    return await news_crud.create(news, session)


@router.put("/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: int,
    news_data: NewsUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    news = await news_crud.get_by_id(news_id, session)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    logger.info("Updating news %s", news_id)
    return await news_crud.update(news, news_data, session)


@router.delete("/{news_id}", status_code=204)
async def delete_news(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    news = await news_crud.get_by_id(news_id, session)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    await news_crud.delete(news, session)
    logger.info("Deleted news %s", news_id)
    return Response(status_code=204)



