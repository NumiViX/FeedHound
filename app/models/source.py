from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=True)
    rss_url = Column(String, unique=True, nullable=True)
    news = relationship(
        "News",
        back_populates="source",
        cascade="all, delete-orphan"
    )
