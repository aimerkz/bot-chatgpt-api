import asyncio
from datetime import datetime, timedelta
from pathlib import Path


async def cleanup_logs():
    logs_dir: Path = Path('logs')
    days_to_keep: int = 3
    check_interval: int = 86400

    while True:
        now = datetime.now()

        for folder in logs_dir.iterdir():
            if folder.is_dir():
                folder_date = datetime.strptime(folder.name, '%Y-%m-%d')

                if now - folder_date > timedelta(days=days_to_keep):
                    for log_file in folder.glob('*.txt'):
                        log_file.unlink()
                    folder.rmdir()

        await asyncio.sleep(check_interval)
