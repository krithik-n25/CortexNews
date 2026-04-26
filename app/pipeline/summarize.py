from typing import List, Dict, Any
from app.services import ai_service
from app.core.logger import get_logger

logger = get_logger(__name__)

def run(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    logger.info("Pipeline Step: Summarize - Starting")
    
    if not articles:
        logger.info("No articles to summarize.")
        return {"insights": [], "trend": ""}
        
    try:
        result = ai_service.summarize_articles(articles)
        num_insights = len(result.get('insights', []))
        logger.info(f"Pipeline Step: Summarize - Completed. Generated {num_insights} insights.")
        return result
    except Exception as e:
        logger.error(f"Pipeline Step: Summarize - Error: {e}")
        return {"insights": [], "trend": ""}
