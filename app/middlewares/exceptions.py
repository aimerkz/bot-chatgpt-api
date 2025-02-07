from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest

from exceptions.openai import (
    BadRequestOIException,
    NotFoundOIException,
    PermissionOIException,
    RateLimitImageOIException,
    ServerOIException,
)
from inlines.actions import get_initial_keyboard

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Message, TelegramObject


class OpenAIExceptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[['TelegramObject', Dict[str, Any]], Awaitable[Any]],
        event: 'Message',
        data: dict[str, Any],
    ):
        state: Optional['FSMContext'] = data.get('state')

        try:
            await handler(event, data)
        except (
            PermissionOIException,
            NotFoundOIException,
            BadRequestOIException,
            RateLimitImageOIException,
            ServerOIException,
            TelegramBadRequest,
        ) as error:
            await self._handle_exception(event, error, state)

    async def _handle_exception(
        self,
        event: 'Message',
        exception: Exception,
        state: 'FSMContext',
    ):
        error_messages = {
            PermissionOIException: '🚫 У тебя нет прав для выполнения этого действия. Проверь ключик API или используй VPN',
            NotFoundOIException: '⚠️ Проверь ссылку на API ChatGTP',
            BadRequestOIException: '❌ Проверь запрос к API ChatGPT',
            RateLimitImageOIException: '😱 Слишком много запросов для генерации изображений',
            ServerOIException: '😞 У ChatGPT какие-то проблемы, попробуй позже',
            TelegramBadRequest: '😢 Не получилось отправить ответ, попробуй позже',
        }

        error_message = error_messages.get(type(exception), '💔 Что-то пошло не так(')
        await event.answer(error_message)
        await self.return_to_main_menu(event, state)

    @staticmethod
    async def return_to_main_menu(event: 'Message', state: 'FSMContext') -> None:
        await event.answer(
            text='Попробуем начать заново 😊',
            reply_markup=get_initial_keyboard(),
        )
        await state.clear()
