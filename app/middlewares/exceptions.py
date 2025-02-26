from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware

from exceptions.openai import (
    BadRequestOIException,
    NotFoundOIException,
    PermissionOIException,
    RateLimitOIException,
    ServerOIException,
)
from keyboards.actions import get_initial_keyboard

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
        try:
            await handler(event, data)
        except (
            PermissionOIException,
            NotFoundOIException,
            BadRequestOIException,
            RateLimitOIException,
            ServerOIException,
        ) as error:
            await self._handle_exception(data['state'], event, error)

    async def _handle_exception(
        self,
        state: 'FSMContext',
        event: 'Message',
        exception: Exception,
    ):
        error_messages = {
            PermissionOIException: '🚫 У тебя нет прав для выполнения этого действия. Проверь ключик API',
            NotFoundOIException: '⚠️ Проверь ссылку на API ChatGTP',
            BadRequestOIException: '❌ Проверь запрос к API ChatGPT',
            RateLimitOIException: '😱 Слишком много запросов к ChatGPT',
            ServerOIException: '😞 У ChatGPT какие-то проблемы, попробуй позже',
        }

        error_message = error_messages.get(type(exception), '💔 Что-то пошло не так(')
        await event.answer(error_message)
        await self.return_to_main_menu(event, state)

    @staticmethod
    async def return_to_main_menu(event: 'Message', state: 'FSMContext') -> None:
        await state.clear()
        await event.answer(
            text='Попробуем начать заново 😊',
            reply_markup=get_initial_keyboard(event),
        )
