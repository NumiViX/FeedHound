from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=True)