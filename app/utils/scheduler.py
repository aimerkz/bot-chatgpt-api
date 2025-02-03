from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.logs import cleanup_logs

scheduler = AsyncIOScheduler(timezone='UTC')


def start_scheduler():
    scheduler.add_job(cleanup_logs, trigger='cron', hour=2, minute=0, max_instances=1)
    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown()
