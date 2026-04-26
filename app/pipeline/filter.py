from typing import List, Dict, Any
from app.core.logger import get_logger
from app.core.constants import FILTER_KEYWORDS, MAX_ARTICLES
from app.db.repository import is_article_seen

logger = get_logger(__name__)

def _is_relevant(article: Dict[str, Any]) -> bool:
    text_to_search = (article.get('title', '') + " " + article.get('description', '')).lower()
    
    # If no keywords defined, pass everything
    if not FILTER_KEYWORDS:
        return True
        
    for keyword in FILTER_KEYWORDS:
        if keyword in text_to_search:
            return True
            
    return False

def run(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logger.info("Pipeline Step: Filter - Starting")
    
    if not articles:
        logger.info("No articles to filter.")
        return []

    filtered_articles = []
    seen_hashes = set()

    for article in articles:
        url = article.get('url', '')
        title = article.get('title', '')
        source = article.get('source', '')
        article_hash = article.get('hash', '')

        # 1. Intra-batch deduplication
        if article_hash in seen_hashes:
            continue
        
        # 2. Relevancy check
        if not _is_relevant(article):
            continue

        # 3. Database memory check
        if is_article_seen(url=url, title=title, source=source):
            continue
            
        seen_hashes.add(article_hash)
        filtered_articles.append(article)
        
        if len(filtered_articles) >= MAX_ARTICLES:
            break

    logger.info(f"Pipeline Step: Filter - Completed. Retained {len(filtered_articles)}/{len(articles)} articles.")
    return filtered_articles
