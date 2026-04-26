import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any
from newsapi import NewsApiClient
import feedparser
from app.core.config import NEWS_API_KEY
from app.core.logger import get_logger
from app.core.constants import NEWS_SOURCES, RSS_FEEDS

logger = get_logger(__name__)

# Initialize News API client
newsapi = NewsApiClient(api_key=NEWS_API_KEY) if NEWS_API_KEY else None

def generate_hash(title: str, source: str) -> str:
    return hashlib.sha256(f"{title}{source}".encode('utf-8')).hexdigest()

def normalize_article(title: str, url: str, source: str, published_at_str: str, description: str, content: str = "") -> dict:
    try:
        # Simple attempt to parse date, might need more robust parsing depending on feed format
        # Many APIs return ISO 8601 strings
        if 'T' in published_at_str and 'Z' in published_at_str:
            published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
        else:
             published_at = datetime.utcnow()
    except Exception:
        published_at = datetime.utcnow()

    return {
        "title": title or "",
        "description": description or "",
        "content": content or "",
        "url": url or "",
        "source": source or "",
        "published_at": published_at,
        "hash": generate_hash(title or "", source or "")
    }

def _parse_newsapi_response(response) -> List[Dict[str, Any]]:
    articles = []
    if response and response.get('status') == 'ok':
        for item in response.get('articles', []):
            articles.append(normalize_article(
                title=item.get('title', ''),
                url=item.get('url', ''),
                source=item.get('source', {}).get('name', 'NewsAPI'),
                published_at_str=item.get('publishedAt', ''),
                description=item.get('description', ''),
                content=item.get('content', '')
            ))
    return articles

def fetch_from_news_api() -> List[Dict[str, Any]]:
    if not newsapi:
        logger.warning("NEWS_API_KEY not set. Skipping NewsAPI fetch.")
        return []

    articles = []
    
    # Only fetch articles from the last 3 days (72 hours)
    since = (datetime.utcnow() - timedelta(hours=72)).strftime('%Y-%m-%dT%H:%M:%S')

    # Query 1: AI news from trusted domains
    try:
        domains = ",".join(NEWS_SOURCES)
        response = newsapi.get_everything(
            q='AI OR "artificial intelligence" OR "machine learning" OR LLM OR "deep learning"',
            domains=domains,
            from_param=since,
            language='en',
            sort_by='publishedAt',
            page_size=50
        )
        articles.extend(_parse_newsapi_response(response))
        logger.info(f"NewsAPI query 1 (domains): {len(articles)} articles")
    except Exception as e:
        logger.error(f"Error fetching from NewsAPI (domains query): {e}")

    # Query 2: Top headlines in technology category
    try:
        response = newsapi.get_top_headlines(
            category='technology',
            language='en',
            page_size=50
        )
        new_articles = _parse_newsapi_response(response)
        articles.extend(new_articles)
        logger.info(f"NewsAPI query 2 (top headlines): {len(new_articles)} articles")
    except Exception as e:
        logger.error(f"Error fetching from NewsAPI (top headlines): {e}")

    return articles

def fetch_from_rss() -> List[Dict[str, Any]]:
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:15]: # limit per feed
                articles.append(normalize_article(
                    title=entry.get('title', ''),
                    url=entry.get('link', ''),
                    source=feed.feed.get('title', feed_url),
                    published_at_str=entry.get('published', ''),
                    description=entry.get('summary', ''),
                    content=""
                ))
        except Exception as e:
            logger.error(f"Error fetching RSS {feed_url}: {e}")
    return articles

def fetch_articles() -> List[Dict[str, Any]]:
    logger.info("Starting article fetch from all sources.")
    all_articles = []
    
    news_api_articles = fetch_from_news_api()
    logger.info(f"Fetched {len(news_api_articles)} articles from NewsAPI.")
    all_articles.extend(news_api_articles)
    
    rss_articles = fetch_from_rss()
    logger.info(f"Fetched {len(rss_articles)} articles from RSS feeds.")
    all_articles.extend(rss_articles)
    
    logger.info(f"Total raw articles fetched: {len(all_articles)}")
    return all_articles
