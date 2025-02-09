from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware

from middlewares.logs_middleware.loggers.factory import LoggerFactory
from utils.enums import BotEnvEnum

if TYPE_CHECKING:
    from aiogram.types import TelegramObject, Update


class LoggingMiddleware(BaseMiddleware):
    max_length_text: int = 50

    def __init__(self, bot_env: BotEnvEnum) -> None:
        self.logger = LoggerFactory().get_logger(bot_env).logger
        super().__init__()

    async def __call__(
        self,
        handler: Callable[['TelegramObject', Dict[str, Any]], Awaitable[Any]],
        event: 'Update',
        data: Dict[str, Any],
    ):
        text_message: str = event.message.text or ''
        text_message = (
            text_message
            if len(text_message) < self.max_length_text
            else text_message[: self.max_length_text]
        )

        self.logger.info(
            f'Получено сообщение от {event.message.from_user.full_name}: {text_message}'
        )

        return await handler(event, data)
