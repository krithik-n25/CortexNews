# AI News WhatsApp Agent

A Python backend that runs a daily pipeline to fetch AI news, summarize it using OpenAI, and send a structured daily brief via WhatsApp using Twilio.

## Setup

1. Clone the repository
2. Set up a virtual environment and install dependencies using `uv`:
   ```bash
   uv venv
   .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys:
   - `OPENAI_API_KEY`
   - `NEWS_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_FROM`
   - `TWILIO_WHATSAPP_TO`

## Running

To run the scheduler (runs daily at the configured time):
```bash
python main.py
```

To trigger the pipeline immediately (for testing):
```bash
python main.py --run-now
```
Or use the script:
```bash
python scripts/run_pipeline.py
```

## Architecture
- **Ingestion**: Fetches articles from NewsAPI and RSS feeds.
- **Filtering**: Removes duplicates and irrelevant articles.
- **Intelligence**: Summarizes top articles into insights using OpenAI.
- **Formatting**: Formats insights into a WhatsApp message.
- **Delivery**: Sends the message via Twilio.
- **Memory**: Stores processed articles in SQLite to prevent duplicates across runs.
