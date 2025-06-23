from sqlalchemy.orm import Session
import logging

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate

logger = logging.getLogger(__name__)


class SourceSyncCRUD:
    def get_by_id(self, source_id: int, session: Session) -> Source | None:
        source = session.query(Source).filter(Source.id == source_id).first()
        logger.debug("Fetched source %s: %s", source_id, bool(source))
        return source

    def get_by_url(self, url: str, session: Session) -> Source | None:
        source = session.query(Source).filter(Source.url == url).first()
        logger.debug("Fetched source by url %s: %s", url, bool(source))
        return source

    def create(self, source_data: SourceCreate, session: Session) -> Source:
        source = Source(**source_data.model_dump())
        session.add(source)
        session.commit()
        session.refresh(source)
        logger.debug("Created source %s", source.id)
        return source

    def update(
        self,
        source: Source,
        source_data: SourceUpdate,
        session: Session
    ) -> Source:
        for key, value in source_data.model_dump(
            exclude_unset=True
        ).items():
            setattr(source, key, value)
        session.commit()
        session.refresh(source)
        logger.debug("Updated source %s", source.id)
        return source


sync_source_crud = SourceSyncCRUD()

