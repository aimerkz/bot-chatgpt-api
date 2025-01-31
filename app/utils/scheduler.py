from app.bot import scheduler
from app.utils.logs import cleanup_logs


def start_scheduler():
    scheduler.add_job(cleanup_logs, trigger='cron', hour=2, minute=0, max_instances=1)
    scheduler.start()
