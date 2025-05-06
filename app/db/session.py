from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_async_engine(
    settings.database_url,
    future=True,
    echo=True
)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False)

sync_engine = create_engine(
    settings.database_url,
    echo=False,
    future=True
)

sync_session_maker = sessionmaker(
    bin=sync_engine,
    autoflush=False,
    autocommit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
