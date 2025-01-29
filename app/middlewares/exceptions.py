from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.exceptions.openai import (
    BadRequestOIException,
    NotFoundOIException,
    PermissionOIException,
    RateLimitImageOIException,
    ServerOIException,
)
from app.inlines.actions import get_initial_keyboard


class OpenAIExceptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ):
        state: FSMContext = data.get('state')

        try:
            await handler(event, data)
        except (
            PermissionOIException,
            NotFoundOIException,
            BadRequestOIException,
            RateLimitImageOIException,
            ServerOIException,
        ) as error:
            await self._handle_exception(event, error, state)

    async def _handle_exception(
        self,
        event: Message,
        exception: Exception,
        state: FSMContext,
    ):
        error_messages = {
            PermissionOIException: '🚫 У тебя нет прав для выполнения этого действия. Проверь ключик API или используй VPN',
            NotFoundOIException: '⚠️ Проверь ссылку на API ChatGTP',
            BadRequestOIException: '❌ Проверь запрос к API ChatGPT',
            RateLimitImageOIException: '😱 Слишком много запросов для генерации изображений',
            ServerOIException: '😞 У ChatGPT какие-то проблемы, попробуй позже',
        }

        error_message = error_messages.get(type(exception), '💔 Что-то пошло не так(')
        await event.answer(error_message)
        await self.return_to_main_menu(event, state)

    @staticmethod
    async def return_to_main_menu(event: Message, state: FSMContext):
        await event.answer(
            text='Попробуем начать заново 😊',
            reply_markup=get_initial_keyboard(),
        )
        await state.clear()
