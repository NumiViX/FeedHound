from sqlalchemy.orm import Session
import logging

from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate

logger = logging.getLogger(__name__)


class NewsSyncCRUD:
    def get_by_id(self, news_id: int, session: Session) -> News | None:
        news = session.query(News).filter(News.id == news_id).first()
        logger.debug("Fetched news %s: %s", news_id, bool(news))
        return news

    def get_by_url(self, url: str, session: Session) -> News | None:
        news = session.query(News).filter(News.url == url).first()
        logger.debug("Fetched news by url %s: %s", url, bool(news))
        return news

    def create(self, news_data: NewsCreate, session: Session) -> News:
        news = News(**news_data.model_dump())
        session.add(news)
        session.commit()
        session.refresh(news)
        logger.debug("Created news %s", news.id)
        return news

    def update(
        self,
        news: News,
        news_data: NewsUpdate,
        session: Session
    ) -> News:
        for key, value in news_data.model_dump(exclude_unset=True).items():
            setattr(news, key, value)
        session.commit()
        session.refresh(news)
        logger.debug("Updated news %s", news.id)
        return news

    def delete(self, news: News, session: Session) -> None:
        session.delete(news)
        session.commit()
        logger.debug("Deleted news %s", news.id)


sync_news_crud = NewsSyncCRUD()

