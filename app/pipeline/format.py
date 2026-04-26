from datetime import datetime
from typing import Dict, Any
from app.core.logger import get_logger

logger = get_logger(__name__)

def run(structured_data: Dict[str, Any]) -> str:
    logger.info("Pipeline Step: Format - Starting")
    
    insights = structured_data.get('insights', [])
    trend = structured_data.get('trend', '')
    
    if not insights:
        logger.warning("No insights provided to format.")
        return ""
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    lines = []
    lines.append(f"🚀 AI Brief – {today_str}\n")
    
    for i, insight in enumerate(insights):
        lines.append(f"{i+1}. {insight.get('headline', 'Headline')}")
        lines.append(f"→ Summary: {insight.get('summary', '')}")
        lines.append(f"→ Why it matters: {insight.get('why_it_matters', '')}")
        source = insight.get('source', '')
        if source:
            lines.append(f"→ Source: {source}")
        url = insight.get('url', '')
        if url:
            lines.append(f"🔗 {url}")
        lines.append("") # Empty line between insights
        
    if trend:
        lines.append("🧠 Trend Insight:")
        lines.append(trend)
        lines.append("")
        
    lines.append("⏱ Read Time: ~2 min")
    
    formatted_message = "\n".join(lines)
    logger.info("Pipeline Step: Format - Completed.")
    
    return formatted_message
