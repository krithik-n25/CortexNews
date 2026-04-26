import time
from app.pipeline import ingest, filter, cluster, summarize, format
from app.services import whatsapp_service
from app.db import repository
from app.core.logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    logger.info("--- Pipeline Execution Started ---")
    start_time = time.time()
    
    try:
        # Step 1: Ingestion
        raw_articles = ingest.run()
        if not raw_articles:
            logger.warning("Pipeline Aborted: No articles ingested.")
            return

        # Step 2: Filtering & Deduplication
        filtered_articles = filter.run(raw_articles)
        if not filtered_articles:
            logger.warning("Pipeline Aborted: No articles remained after filtering.")
            return
            
        # Step 3: Clustering (Pass-through for now)
        clustered_articles = cluster.run(filtered_articles)
        
        # Step 4: Summarization & Intelligence
        structured_data = summarize.run(clustered_articles)
        if not structured_data or not structured_data.get('insights'):
            logger.warning("Pipeline Aborted: Failed to generate insights.")
            return

        # Step 5: Formatting
        message = format.run(structured_data)
        if not message:
            logger.warning("Pipeline Aborted: Failed to format message.")
            return

        # Step 6: Delivery
        logger.info("Pipeline Step: Delivery - Starting")
        success = whatsapp_service.send_message(message)
        if success:
            logger.info("Pipeline Step: Delivery - Completed Successfully")
            
            # Save state only on successful delivery to avoid skipping on retry
            repository.save_articles(filtered_articles)
            repository.save_insights(structured_data.get('insights', []))
            repository.save_trend(structured_data.get('trend', ''))
            logger.info("Database state updated.")
        else:
            logger.error("Pipeline Step: Delivery - Failed")

    except Exception as e:
        logger.error(f"Pipeline Execution Failed with error: {e}", exc_info=True)
        
    finally:
        elapsed = time.time() - start_time
        logger.info(f"--- Pipeline Execution Finished in {elapsed:.2f} seconds ---")
