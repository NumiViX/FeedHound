from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from app.models.news import News
from app.schemas.news import NewsCreate


class NewsCRUD:
    async def create_news(
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
        return news

    async def get_all_news(self, session: AsyncSession) -> List[News]:
        result = await session.execute(select(News))
        return result.scalars().all()

    async def get_news_by_id(
        self,
        news_id: int,
        session: AsyncSession
    ) -> Optional[News]:
        result = await session.execute(select(News).where(News.id == news_id))
        return result.scalar_one_or_none()

    async def update_news(
        self,
        news: News,
        news_data: NewsCreate,
        session: AsyncSession
    ) -> News:
        news.title = news_data.title
        news.published_at = news_data.published_at
        news.url = str(news_data.url)
        news.source_id = news_data.source_id
        await session.commit()
        await session.refresh(news)
        return news

    async def delete_news(self, news: News, session: AsyncSession) -> None:
        await session.delete(news)
        await session.commit()


news_crude = NewsCRUD()
