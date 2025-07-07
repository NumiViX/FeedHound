from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import logging

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
    bind=sync_engine,
    autoflush=False,
    autocommit=False
)

logger = logging.getLogger(__name__)


async def get_async_session() -> AsyncSession:
    logger.debug("Creating async DB session")
    async with async_session() as session:
        yield session

