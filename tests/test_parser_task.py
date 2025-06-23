import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.source import Source
from app.models.news import News
from app.schemas.news import NewsCreate
from app.tasks.parser import parse_source_task


# create shared in-memory database
engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(engine)


@contextmanager
def in_memory_session():
    with SessionLocal() as session:
        yield session


def test_parse_source_task_creates_news(monkeypatch):
    # patch session maker used by the task
    monkeypatch.setattr("app.tasks.parser.sync_session_maker", in_memory_session)

    # Prepopulate database with a source and one existing news entry
    with in_memory_session() as session:
        source = Source(url="https://example.com", title="Example", rss_url="https://example.com/rss")
        session.add(source)
        session.commit()
        session.refresh(source)
        existing = News(
            title="Old",
            url="https://exists.com/news",
            published_at=datetime.datetime.now(datetime.timezone.utc),
            source_id=source.id,
        )
        session.add(existing)
        session.commit()
        source_id = source.id

    predefined = [
        NewsCreate(
            title="Old",
            url="https://exists.com/news",
            published_at=datetime.datetime.now(datetime.timezone.utc),
            source_id=source_id,
        ),
        NewsCreate(
            title="New",
            url="https://new.com/news",
            published_at=datetime.datetime.now(datetime.timezone.utc),
            source_id=source_id,
        ),
    ]

    def fake_parser(s_id: int, rss: str):
        return predefined

    monkeypatch.setattr("app.tasks.parser.parse_news_sync", fake_parser)

    parse_source_task(source_id)

    with in_memory_session() as session:
        urls = sorted(n.url for n in session.query(News).all())
        assert urls == ["https://exists.com/news", "https://new.com/news"]
