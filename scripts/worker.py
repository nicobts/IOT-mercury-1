from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from datetime import datetime

from src.services.data_collector import DataCollector
from src.config import config
from src.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def collect_usage_job():
    """Scheduled job to collect usage data"""
    logger.info("Starting usage data collection...")
    try:
        collector = DataCollector()
        collector.collect_all_usage_data(days_back=1)
        logger.info("Usage data collection completed")
    except Exception as e:
        logger.error(f"Usage data collection failed: {e}")


def full_sync_job():
    """Scheduled job for full SIM sync"""
    logger.info("Starting full SIM sync...")
    try:
        collector = DataCollector()
        result = collector.sync_all_sims()
        logger.info(f"Full sync completed: {result}")
    except Exception as e:
        logger.error(f"Full sync failed: {e}")


def main():
    scheduler = BlockingScheduler()

    # Collect usage data every hour
    scheduler.add_job(
        collect_usage_job,
        trigger=IntervalTrigger(
            minutes=config.DATA_COLLECTION_INTERVAL_MINUTES
        ),
        id='collect_usage',
        name='Collect usage data',
        replace_existing=True
    )

    # Full sync once per day at 2 AM
    scheduler.add_job(
        full_sync_job,
        trigger='cron',
        hour=2,
        minute=0,
        id='full_sync',
        name='Full SIM sync',
        replace_existing=True
    )

    logger.info("Starting scheduler...")
    logger.info(f"Usage collection interval: {config.DATA_COLLECTION_INTERVAL_MINUTES} minutes")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    main()
