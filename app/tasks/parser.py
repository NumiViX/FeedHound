from celery import shared_task
import logging

from app.db.session import sync_session_maker
from app.crud.sync_news import sync_news_crud
from app.crud.sync_source import sync_source_crud
from app.parsers.sync_news_parser import parse_news_sync

logger = logging.getLogger(__name__)


@shared_task
def parse_source_task(source_id: int):
    logger.info("Parsing source %s", source_id)
    with sync_session_maker() as session:
        source = sync_source_crud.get_by_id(source_id, session)
        if not source or not source.rss_url:
            logger.warning("Source %s missing or has no RSS URL", source_id)
            return

        news_list = parse_news_sync(source.id, source.rss_url)
        for news in news_list:
            if not sync_news_crud.get_by_url(news.url, session):
                sync_news_crud.create(news, session)
                logger.debug("Created news %s", news.url)

