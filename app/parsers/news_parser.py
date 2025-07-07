from datetime import datetime, timezone
import logging
import feedparser

from app.schemas.news import NewsCreate


async def parse_news(
    source_id: int,
    rss_url: str
) -> list[NewsCreate]:
    """
    Парсер для RSS-ленты.
    """
    logger = logging.getLogger(__name__)
    logger.debug("Parsing RSS feed %s", rss_url)
    feed = feedparser.parse(rss_url)
    news = []
    for entry in feed.entries:
        published_at = (
            datetime(*entry.published_parsed[:6])
            if "published_parsed" in entry
            else datetime.now(timezone.utc)
        )
        news.append(
            NewsCreate(
                title=entry.title,
                url=entry.link,
                published_at=published_at,
                source_id=source_id,
            )
        )
    return news

