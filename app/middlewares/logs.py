import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class LoggingMiddleware(BaseMiddleware):
    max_length_text: int = 50
    logs_dir: str = 'logs'
    log_filename: str = 'logs.log'

    def __init__(
        self,
        logger: logging.Logger = None,
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self._setup_handler()

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

    def _setup_handler(self):
        os.makedirs(self.logs_dir, exist_ok=True)
        log_path = os.path.join(self.logs_dir, self.log_filename)

        handler = TimedRotatingFileHandler(
            log_path,
            when='MIDNIGHT',
            interval=1,
            backupCount=3,
            encoding='utf-8',
            utc=True,
        )
        handler.namer = self._flip_name

        handler.setFormatter(
            logging.Formatter(
                fmt='[%(asctime)s] [%(name)s] [%(levelname)s] > [%(message)s]',
                datefmt='%Y-%m-%d %H:%M:%S',
            )
        )

        self.logger.addHandler(handler)

    @staticmethod
    def _flip_name(log_path: str):
        log_dir, log_filename = os.path.split(log_path)
        _, timestamp = log_filename.rsplit('.', 1)
        return os.path.join(log_dir, f'logs-{timestamp}.log')
