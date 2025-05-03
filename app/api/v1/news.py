from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_async_session
from app.crud.news import news_crude
from app.schemas.news import NewsCreate, NewsRead, NewsUpdate

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/", response_model=List[NewsRead])
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    return await news_crude.get_all_news(session)


@router.get("/{news_id}", response_model=NewsRead)
async def get_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    news = await news_crude.get_news_by_id(news_id, session)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.post("/", response_model=NewsRead, status_code=201)
async def create_news(
    news: NewsCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await news_crude.create_news(news, session)


@router.put("/{news_id}", response_model=NewsUpdate)
async def update_news(
    news_id: int,
    news_data: NewsUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    news = await news_crude.get_news_by_id(news_id, session)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return await news_crude.update_news(news, news_data, session)


@router.delete("/{news_id}", status_code=204)
async def delete_news(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    news = await news_crude.get_news_by_id(news_id, session)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    await news_crude.delete_news(news, session)
    return HTTPException(status_code=204, detail="Source deleted")



