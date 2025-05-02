from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.source import Source
from app.schemas.source import SourceCreate


async def create_source(
    session: AsyncSession,
    source_data: SourceCreate
) -> Source:

    source_data = source_data.model_dump()
    source_data["url"] = str(source_data["url"])
    new_source = Source(**source_data)
    session.add(new_source)
    await session.commit()
    await session.refresh(new_source)

    return new_source


async def get_sources(
    session: AsyncSession
) -> list[Source]:

    result = await session.execute(select(Source))

    return result.scalars().all()
