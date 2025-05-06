from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate


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

        return new_source

    async def get(
        self,
        session: AsyncSession
    ) -> list[Source]:
        result = await session.execute(select(Source))
        return result.scalars().all()

    async def get_by_id(
        self,
        source_id: int,
        session: AsyncSession
    ) -> Source | None:
        data = select(Source).where(Source.id == source_id)
        result = await session.execute(data)
        return result.scalar_one_or_none()

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
        return source

    async def delete(
        self,
        source: Source,
        session: AsyncSession
    ) -> None:
        await session.delete(source)
        await session.commit()


source_crud = SourceCRUD()
