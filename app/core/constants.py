MAX_ARTICLES = 50
MAX_INSIGHTS = 7

# Domains for NewsAPI queries
NEWS_SOURCES = [
    "techcrunch.com",
    "wired.com",
    "theverge.com",
    "venturebeat.com",
    "arstechnica.com",
    "thenextweb.com",
    "zdnet.com",
    "engadget.com",
    "reuters.com",
    "bloomberg.com",
    "forbes.com",
    "cnbc.com",
    "bbc.com",
]

# RSS feeds — AI-focused blogs, research orgs, and aggregators
RSS_FEEDS = [
    # MIT Technology Review — AI section
    "https://www.technologyreview.com/feed/",
    # Google AI Blog
    "https://blog.research.google/feeds/posts/default?alt=rss",
    # OpenAI Blog
    "https://openai.com/blog/rss.xml",
    # Hacker News — front page (lots of AI discussion)
    "https://hnrss.org/frontpage",
    # AI-specific subreddit
    "https://www.reddit.com/r/artificial/.rss",
    # Machine Learning subreddit
    "https://www.reddit.com/r/MachineLearning/.rss",
    # Slashdot
    "https://rss.slashdot.org/Slashdot/slashdotMain",
    # The Verge — AI tag
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    # Ars Technica — AI
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
    # TechCrunch — AI category
    "https://techcrunch.com/category/artificial-intelligence/feed/",
]

FILTER_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "ml",
    "deep learning", "llm", "large language model", "openai",
    "anthropic", "google deepmind", "startup funding", "neural network",
    "chatgpt", "claude", "gemini", "gpt", "transformer",
    "diffusion model", "computer vision", "nlp", "natural language",
    "robotics", "autonomous", "generative ai", "foundation model",
    "meta ai", "mistral", "llama", "stable diffusion", "midjourney",
    "copilot", "agent", "rag", "retrieval augmented", "fine-tuning",
    "hugging face", "nvidia", "gpu", "tpu", "inference",
]
