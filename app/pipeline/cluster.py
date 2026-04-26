from typing import List, Dict, Any
from app.core.logger import get_logger

logger = get_logger(__name__)

def run(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Stub for future clustering (Phase 2).
    Currently just returns articles as-is.
    """
    logger.info("Pipeline Step: Cluster - Starting (Pass-through)")
    logger.info(f"Pipeline Step: Cluster - Completed. Returning {len(articles)} articles.")
    return articles
