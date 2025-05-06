from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.crud.source import source_crud
from app.crud.news import news_crude
from app.parsers.news_parser import parse_news
from app.schemas.news import NewsRead
from app.schemas.source import SourceCreate, SourceRead, SourceUpdate

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/", response_model=SourceRead)
async def create(
    source: SourceCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await source_crud.create(source, session)


@router.get("/", response_model=list[SourceRead])
async def read(session: AsyncSession = Depends(get_async_session)):
    return await source_crud.get(session)


@router.get("/{source_id}", response_model=SourceRead)
async def get_source_by_id(
    source_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    source = await source_crud.get_by_id(source_id, session)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.put("/{source_id}", response_model=SourceRead)
async def update_source(
    source_id: int,
    source_data: SourceUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    source = await source_crud.get_by_id(source_id, session)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return await source_crud.update(source, source_data, session)


@router.delete("/source_id")
async def delete_source(
    source_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    source = await source_crud.get_by_id(source_id, session)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    await source_crud.delete(source, session)
    return {"detail: Source deleted"}


@router.post("/{source_id}/parse")
async def parse_source(
    source_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> list[NewsRead]:
    source = await source_crud.get_by_id(source_id, session)
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    news_items = await parse_news(source.id, source.rss_url)

    created_news = []
    for item in news_items:
        created_news.append(await news_crude.create(item, session))

    return created_news
