import argparse
from app.db.repository import init_db
from app.scheduler.cron_jobs import start_scheduler
from app.pipeline.orchestrator import run_pipeline
from app.core.logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="AI News WhatsApp Agent")
    parser.add_argument('--run-now', action='store_true', help='Run the pipeline immediately once, instead of starting the scheduler')
    args = parser.parse_args()

    # Ensure DB is initialized
    init_db()

    if args.run_now:
        logger.info("Starting manual pipeline run...")
        run_pipeline()
    else:
        logger.info("Starting scheduler...")
        start_scheduler()

if __name__ == "__main__":
    main()
