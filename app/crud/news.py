from typing import List, Optional
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate

logger = logging.getLogger(__name__)


class NewsCRUD:
    async def create(
        self,
        news_data: NewsCreate,
        session: AsyncSession
    ) -> News:
        news = News(
            title=news_data.title,
            url=str(news_data.url),
            published_at=news_data.published_at,
            source_id=news_data.source_id
        )
        session.add(news)
        await session.commit()
        await session.refresh(news)
        logger.debug("Created news %s", news.id)
        return news

    async def get_all(self, session: AsyncSession) -> List[News]:
        result = await session.execute(select(News))
        news = result.scalars().all()
        logger.debug("Fetched %d news items", len(news))
        return news

    async def get_by_id(
        self,
        news_id: int,
        session: AsyncSession
    ) -> Optional[News]:
        result = await session.execute(select(News).where(News.id == news_id))
        news = result.scalar_one_or_none()
        logger.debug("Fetched news by id %s: %s", news_id, bool(news))
        return news

    async def update(
        self,
        news: News,
        news_data: NewsUpdate,
        session: AsyncSession
    ) -> News:
        news.title = news_data.title
        news.published_at = news_data.published_at
        news.url = str(news_data.url)
        news.source_id = news_data.source_id
        await session.commit()
        await session.refresh(news)
        logger.debug("Updated news %s", news.id)
        return news

    async def delete(self, news: News, session: AsyncSession) -> None:
        await session.delete(news)
        await session.commit()
        logger.debug("Deleted news %s", news.id)


news_crude = NewsCRUD()

