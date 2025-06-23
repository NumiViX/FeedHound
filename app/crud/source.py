from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate

logger = logging.getLogger(__name__)


class SourceCRUD:
    async def create(
        self,
        source_data: SourceCreate,
        session: AsyncSession
    ) -> Source:

        source_data = source_data.model_dump()
        new_source = Source(**source_data)
        session.add(new_source)
        await session.commit()
        await session.refresh(new_source)
        logger.debug("Created source %s", new_source.id)

        return new_source

    async def get(
        self,
        session: AsyncSession
    ) -> list[Source]:
        result = await session.execute(select(Source))
        sources = result.scalars().all()
        logger.debug("Fetched %d sources", len(sources))
        return sources

    async def get_by_id(
        self,
        source_id: int,
        session: AsyncSession
    ) -> Source | None:
        data = select(Source).where(Source.id == source_id)
        result = await session.execute(data)
        source = result.scalar_one_or_none()
        logger.debug("Fetched source by id %s: %s", source_id, bool(source))
        return source

    async def update(
        self,
        source: Source,
        source_data: SourceUpdate,
        session: AsyncSession
    ) -> Source:
        for key, value in source_data.model_dump(exclude_unset=True).items():
            setattr(source, key, value)
        await session.commit()
        await session.refresh(source)
        logger.debug("Updated source %s", source.id)
        return source

    async def delete(
        self,
        source: Source,
        session: AsyncSession
    ) -> None:
        await session.delete(source)
        await session.commit()
        logger.debug("Deleted source %s", source.id)


source_crud = SourceCRUD()

