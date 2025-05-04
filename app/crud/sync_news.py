from sqlalchemy.orm import Session

from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate


class NewsSyncCRUD:
    def get_by_id(self, news_id: int, session: Session) -> News | None:
        return session.query(News).filter(News.id == news_id).first()

    def get_by_url(self, url: str, session: Session) -> News | None:
        return session.query(News).filter(News.url == url).first()

    def create(self, news_data: NewsCreate, session: Session) -> News:
        news = News(**news_data.model_dump())
        session.add(news)
        session.commit()
        session.refresh(news)
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
        return news

    def delete(sels, news: News, session: Session) -> None:
        session.delete(news)
        session.commit()


sync_news_crud = NewsSyncCRUD()
