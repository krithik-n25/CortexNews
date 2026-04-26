from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False, index=True)
    hash = Column(String, nullable=False, index=True)
    source = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Insight(Base):
    __tablename__ = 'insights'

    id = Column(Integer, primary_key=True)
    headline = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Trend(Base):
    __tablename__ = 'trends'

    id = Column(Integer, primary_key=True)
    trend = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
