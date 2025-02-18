from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware

if TYPE_CHECKING:
    from aiogram.types import TelegramObject, Update

    from middlewares.logs_middleware.loggers.base import BaseLogger


class LoggingMiddleware(BaseMiddleware):
    max_length_text: int = 50

    def __init__(self, logger: 'BaseLogger') -> None:
        self.logger = logger.logger
        super().__init__()

    async def __call__(
        self,
        handler: Callable[['TelegramObject', Dict[str, Any]], Awaitable[Any]],
        event: 'Update',
        data: Dict[str, Any],
    ):
        event_message = event.message
        if event_message:
            text_message: str = event_message.text or ''
            text_message = (
                text_message
                if len(text_message) < self.max_length_text
                else text_message[: self.max_length_text]
            )

            self.logger.info(
                f'Получено сообщение от {event.message.from_user.full_name}: {text_message}'
            )

        return await handler(event, data)
