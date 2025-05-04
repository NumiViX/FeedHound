from sqlalchemy.orm import Session

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate


class SourceSyncCRUD:
    def get_by_id(self, source_id: int, session: Session) -> Source | None:
        return session.query(Source).filter(Source.id == source_id).first()

    def get_by_url(self, url: str, session: Session) -> Source | None:
        return session.query(Source).filter(Source.url == url).first()

    def create(self, source_data: SourceCreate, session: Session) -> Source:
        source = Source(**source_data.model_dump())
        session.add(source)
        session.commit()
        session.refresh(source)
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
        return source


sync_source_crud = SourceSyncCRUD()
