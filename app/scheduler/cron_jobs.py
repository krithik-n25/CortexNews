from apscheduler.schedulers.blocking import BlockingScheduler
from app.pipeline.orchestrator import run_pipeline
from app.core.config import PIPELINE_SCHEDULE_HOUR, PIPELINE_SCHEDULE_MINUTE
from app.core.logger import get_logger

logger = get_logger(__name__)

def start_scheduler():
    scheduler = BlockingScheduler()
    
    # Schedule to run every 3 days at the configured time
    scheduler.add_job(
        run_pipeline, 
        'interval', 
        days=3,
        start_date=f'2026-04-26 {PIPELINE_SCHEDULE_HOUR:02d}:{PIPELINE_SCHEDULE_MINUTE:02d}:00',
        misfire_grace_time=3600 # 1 hour grace time
    )
    
    logger.info(f"Scheduler started. Pipeline will run every 3 days at {PIPELINE_SCHEDULE_HOUR:02d}:{PIPELINE_SCHEDULE_MINUTE:02d}")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
