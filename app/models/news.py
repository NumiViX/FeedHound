from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    published_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    source = relationship("Source", back_populates="news")
