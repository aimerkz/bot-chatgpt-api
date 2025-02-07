from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest

from exceptions.openai import (
    BadRequestOIException,
    NotFoundOIException,
    PermissionOIException,
    RateLimitOIException,
    ServerOIException,
)
from keyboards.actions import get_initial_keyboard

if TYPE_CHECKING:
    from aiogram.types import Message, TelegramObject


class OpenAIExceptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[['TelegramObject', Dict[str, Any]], Awaitable[Any]],
        event: 'Message',
        data: dict[str, Any],
    ):
        try:
            await handler(event, data)
        except (
            PermissionOIException,
            NotFoundOIException,
            BadRequestOIException,
            RateLimitOIException,
            ServerOIException,
            TelegramBadRequest,
        ) as error:
            await self._handle_exception(event, error)

    async def _handle_exception(
        self,
        event: 'Message',
        exception: Exception,
    ):
        error_messages = {
            PermissionOIException: '🚫 У тебя нет прав для выполнения этого действия. Проверь ключик API или используй VPN',
            NotFoundOIException: '⚠️ Проверь ссылку на API ChatGTP',
            BadRequestOIException: '❌ Проверь запрос к API ChatGPT',
            RateLimitOIException: '😱 Слишком много запросов к ChatGPT',
            ServerOIException: '😞 У ChatGPT какие-то проблемы, попробуй позже',
            TelegramBadRequest: '😢 Не получилось отправить ответ, попробуй позже',
        }

        error_message = error_messages.get(type(exception), '💔 Что-то пошло не так(')
        await event.answer(error_message)
        await self.return_to_main_menu(event)

    @staticmethod
    async def return_to_main_menu(event: 'Message') -> None:
        await event.answer(
            text='Попробуем начать заново 😊',
            reply_markup=get_initial_keyboard(),
        )
