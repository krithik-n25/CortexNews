import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.repository import init_db
from app.pipeline.orchestrator import run_pipeline
from app.core.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Manual Pipeline Trigger via Script")
    init_db()
    run_pipeline()
