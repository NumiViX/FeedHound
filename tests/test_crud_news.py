import datetime
import pytest

from app.crud.news import NewsCRUD
from app.crud.source import SourceCRUD
from app.schemas.news import NewsCreate, NewsUpdate
from app.schemas.source import SourceCreate


@pytest.mark.asyncio
async def test_news_crud(async_session):
    source = await SourceCRUD().create(
        SourceCreate(title="Src", url="http://s.com", rss_url="http://s.com/rss"),
        async_session,
    )

    crud = NewsCRUD()
    create_data = NewsCreate(
        title="Title",
        url="http://s.com/n1",
        published_at=datetime.datetime.now(datetime.timezone.utc),
        source_id=source.id,
    )
    news = await crud.create(create_data, async_session)
    assert news.id is not None

    all_news = await crud.get_all(async_session)
    assert len(all_news) == 1
    assert all_news[0].id == news.id

    fetched = await crud.get_by_id(news.id, async_session)
    assert fetched.title == "Title"

    updated = await crud.update(
        fetched,
        NewsUpdate(
            title="Updated",
            url="http://s.com/n2",
            published_at=create_data.published_at,
            source_id=source.id,
        ),
        async_session,
    )
    assert updated.title == "Updated"

    await crud.delete(updated, async_session)
    assert await crud.get_by_id(news.id, async_session) is None
