import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY_FALLBACK = os.getenv("GROQ_API_KEY_FALLBACK")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

# Support multiple recipients: comma-separated in .env
_raw_to = os.getenv("TWILIO_WHATSAPP_TO", "")
TWILIO_WHATSAPP_TO = [num.strip() for num in _raw_to.split(",") if num.strip()]

PIPELINE_SCHEDULE_HOUR = int(os.getenv("PIPELINE_SCHEDULE_HOUR", 8))
PIPELINE_SCHEDULE_MINUTE = int(os.getenv("PIPELINE_SCHEDULE_MINUTE", 0))

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "sqlite.db")
DB_URL = f"sqlite:///{DB_PATH}"
