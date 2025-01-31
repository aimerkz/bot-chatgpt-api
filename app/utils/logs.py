from datetime import datetime, timedelta
from pathlib import Path

LOGS_DIR = Path('logs')
DAYS_TO_KEEP = 3


async def cleanup_logs():
    now = datetime.now()

    for folder in LOGS_DIR.iterdir():
        if folder.is_dir():
            folder_date = datetime.strptime(folder.name, '%Y-%m-%d')

            if now - folder_date > timedelta(days=DAYS_TO_KEEP):
                for log_file in folder.glob('*.txt'):
                    log_file.unlink()
                folder.rmdir()
