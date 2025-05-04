from celery import shared_task

from app.db.session import sync_session_maker
from app.crud.sync_news import sync_news_crud
from app.crud.sync_source import sync_source_crud
from app.parsers.sync_news_parser import parse_news_sync


@shared_task
def parse_source_task(source_id: int):
    with sync_session_maker() as session:
        source = sync_source_crud.get_by_id(source_id, session)
        if not source or not source.rss_url:
            return

        news_list = parse_news_sync(source.id, source.rss_url)
        for news in news_list:
            if not sync_news_crud.get_by_url(news.url, session):
                sync_news_crud.create(news, session)
