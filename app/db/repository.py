from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.models import Base, Article, Insight, Trend
from app.core.config import DB_URL
from app.core.logger import get_logger
import hashlib

logger = get_logger(__name__)

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized.")

def get_session() -> Session:
    return SessionLocal()

def is_article_seen(url: str, title: str = "", source: str = "") -> bool:
    with get_session() as session:
        # Check by exact URL
        exists = session.query(Article).filter(Article.url == url).first()
        if exists:
            return True
            
        # Check by Hash (Title + Source) if URL changed slightly
        if title and source:
            article_hash = hashlib.sha256(f"{title}{source}".encode('utf-8')).hexdigest()
            exists_hash = session.query(Article).filter(Article.hash == article_hash).first()
            if exists_hash:
                return True
                
        return False

def save_articles(articles_data: list[dict]):
    with get_session() as session:
        for data in articles_data:
            if not is_article_seen(data.get('url', ''), data.get('title', ''), data.get('source', '')):
                article = Article(
                    title=data.get('title', ''),
                    url=data.get('url', ''),
                    hash=data.get('hash', ''),
                    source=data.get('source', ''),
                    published_at=data.get('published_at')
                )
                session.add(article)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving articles: {e}")

def save_insights(insights_data: list[dict]):
    with get_session() as session:
        for data in insights_data:
            insight = Insight(
                headline=data.get('headline', ''),
                summary=data.get('summary', ''),
                category=data.get('category', '')
            )
            session.add(insight)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving insights: {e}")

def save_trend(trend_text: str):
    if not trend_text:
        return
    with get_session() as session:
        trend = Trend(trend=trend_text)
        session.add(trend)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving trend: {e}")
