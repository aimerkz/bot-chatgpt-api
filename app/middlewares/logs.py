import datetime
import logging
import os
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class LoggingMiddleware(BaseMiddleware):
    max_length_text: int = 50
    logs_path: str = 'logs'

    def __init__(
        self,
        logger: logging.Logger = None,
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        log_dir = os.path.join(self.logs_path, current_date)
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, 'logs.txt')

        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(
            logging.Formatter(
                fmt='[%(asctime)s] [%(name)s] [%(levelname)s] > [%(message)s]',
                datefmt='%Y-%m-%d %H:%M:%S',
            )
        )
        self.logger.addHandler(handler)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ):
        text_message = (
            event.text
            if len(event.text) < self.max_length_text
            else event.text[: self.max_length_text]
        )
        self.logger.info(
            f'Получено сообщение от {event.from_user.full_name}: {text_message}'
        )
        return await handler(event, data)
