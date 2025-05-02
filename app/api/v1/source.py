from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.source import SourceCreate, SourceRead
from app.db.session import get_async_session
from app.crud.source import create_source, get_sources

router = APIRouter()


@router.post("/", response_model=SourceRead)
async def create(
    source: SourceCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await create_source(session, source)


@router.get("/", response_model=list[SourceRead])
async def read(session: AsyncSession = Depends(get_async_session)):
    return await get_sources(session)
