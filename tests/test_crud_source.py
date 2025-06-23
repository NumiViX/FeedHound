import pytest
from app.crud.source import SourceCRUD
from app.schemas.source import SourceCreate, SourceUpdate


@pytest.mark.asyncio
async def test_source_crud(async_session):
    crud = SourceCRUD()
    create_data = SourceCreate(
        title="Example",
        url="http://example.com",
        rss_url="http://example.com/rss",
    )
    source = await crud.create(create_data, async_session)
    assert source.id is not None

    all_sources = await crud.get(async_session)
    assert len(all_sources) == 1
    assert all_sources[0].id == source.id

    fetched = await crud.get_by_id(source.id, async_session)
    assert fetched.title == "Example"

    updated = await crud.update(
        fetched,
        SourceUpdate(title="Updated title"),
        async_session,
    )
    assert updated.title == "Updated title"

    await crud.delete(updated, async_session)
    assert await crud.get_by_id(source.id, async_session) is None
