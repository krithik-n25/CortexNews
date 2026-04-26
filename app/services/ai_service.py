import json
from typing import List, Dict, Any
from groq import Groq
from app.core.config import GROQ_API_KEY, GROQ_API_KEY_FALLBACK
from app.core.logger import get_logger
from app.core.constants import MAX_INSIGHTS

logger = get_logger(__name__)

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def _make_groq_call(current_client: Groq, system_prompt: str, articles_text: str) -> Dict[str, Any]:
    response = current_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here are the latest news articles:\n\n{articles_text}"}
        ],
        response_format={ "type": "json_object" },
        temperature=0.3
    )
    content = response.choices[0].message.content
    return json.loads(content)

def summarize_articles(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not client and not GROQ_API_KEY_FALLBACK:
        logger.error("No Groq API keys set. Cannot summarize.")
        return {"insights": [], "trend": ""}

    if not articles:
        return {"insights": [], "trend": ""}

    logger.info(f"Calling Groq to summarize {len(articles)} articles.")

    # Compress articles into a string for the prompt
    articles_text = ""
    for i, a in enumerate(articles):
        articles_text += f"[{i+1}] Title: {a.get('title')}\n"
        articles_text += f"Source: {a.get('source')}\n"
        articles_text += f"URL: {a.get('url', '')}\n"
        desc = a.get('description', '')
        if desc:
            articles_text += f"Description: {desc[:300]}...\n"
        articles_text += "\n"

    system_prompt = f"""
You are a senior AI intelligence analyst. Your job is to read raw tech news articles and extract the highest-signal insights.
Limit your output to a maximum of {MAX_INSIGHTS} insights.
Exclude opinion pieces, minor updates, and repetitive coverage.
Prioritize major product launches, funding rounds, breakthroughs, and strategic moves.

Output strictly valid JSON with the following schema:
{{
  "insights": [
    {{
      "headline": "Clear, punchy headline",
      "summary": "2-3 sentence concise explanation of what happened",
      "why_it_matters": "Clear business/tech impact in 1-2 lines",
      "category": "e.g., Model Release, Startup Funding, Infrastructure, Research",
      "source": "Name of the publication or source",
      "url": "Direct URL to the original article"
    }}
  ],
  "trend": "1-2 sentence synthesis of the overall pattern or shift observed across the news items"
}}
"""

    try:
        if not client:
            raise Exception("Primary client not initialized.")
        result = _make_groq_call(client, system_prompt, articles_text)
        logger.info(f"Successfully generated {len(result.get('insights', []))} insights with primary key.")
        return result
    except Exception as e:
        logger.warning(f"Primary Groq API failed ({e}). Attempting fallback...")
        if GROQ_API_KEY_FALLBACK:
            try:
                fallback_client = Groq(api_key=GROQ_API_KEY_FALLBACK)
                result = _make_groq_call(fallback_client, system_prompt, articles_text)
                logger.info(f"Successfully generated {len(result.get('insights', []))} insights with fallback key.")
                return result
            except Exception as fallback_e:
                logger.error(f"Fallback Groq API also failed: {fallback_e}")
        else:
             logger.error("No fallback key configured.")
             
        return {"insights": [], "trend": ""}
