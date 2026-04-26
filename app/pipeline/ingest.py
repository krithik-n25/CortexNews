from typing import List, Dict, Any
from app.services import news_service
from app.core.logger import get_logger

logger = get_logger(__name__)

def run() -> List[Dict[str, Any]]:
    logger.info("Pipeline Step: Ingest - Starting")
    try:
        articles = news_service.fetch_articles()
        logger.info(f"Pipeline Step: Ingest - Completed. Total articles fetched: {len(articles)}")
        return articles
    except Exception as e:
        logger.error(f"Pipeline Step: Ingest - Error: {e}")
        return []
