import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ContentType
from aiogram.types import Message


class LoggingMiddleware(BaseMiddleware):
    max_length_text: int = 50
    logs_path: str = 'logs/logs.txt'

    def __init__(
        self,
        logger: logging.Logger = None,
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # os.makedirs(os.path.dirname(self.logs_path), exist_ok=True)

        handler = logging.StreamHandler()
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
        match event.content_type:
            case ContentType.VOICE:
                return await handler(event, data)
            case _:
                text_message = (
                    event.text
                    if len(event.text) < self.max_length_text
                    else event.text[: self.max_length_text]
                )
                self.logger.info(
                    f'Получено сообщение от {event.from_user.full_name}: {text_message}'
                )
                return await handler(event, data)
