from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware

from exceptions import openai as openai_exceptions
from keyboards.actions import get_initial_keyboard
from utils.types import T

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types.message import Message


class OpenAIExceptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[T, Dict[str, Any]], Awaitable[Any]],
        event: T,
        data: dict[str, Any],
    ):
        try:
            await handler(event, data)
        except (
            openai_exceptions.PermissionOIException,
            openai_exceptions.NotFoundOIException,
            openai_exceptions.BadRequestOIException,
            openai_exceptions.RateLimitOIException,
            openai_exceptions.ServerOIException,
            openai_exceptions.AuthenticationOIException,
            openai_exceptions.TimedOutOIException,
        ) as error:
            await self._handle_exception(data['state'], event, error)

    async def _handle_exception(
        self,
        state: 'FSMContext',
        event: 'Message',
        exception: Exception,
    ):
        error_messages = {
            openai_exceptions.PermissionOIException: '🚫 У тебя нет прав для выполнения этого действия. Проверь ключик API',
            openai_exceptions.NotFoundOIException: '⚠️ Проверь ссылку на API ChatGTP',
            openai_exceptions.BadRequestOIException: '❌ Проверь запрос к API ChatGPT',
            openai_exceptions.RateLimitOIException: '😱 Слишком много запросов к ChatGPT',
            openai_exceptions.ServerOIException: '😞 У ChatGPT какие-то проблемы, попробуй позже',
            openai_exceptions.AuthenticationOIException: 'Не получилось авторизоваться :(',
            openai_exceptions.TimedOutOIException: 'Превышено время ожидания ответа от ChatGPT :(',
        }

        error_message = error_messages.get(type(exception), '💔 Что-то пошло не так(')  # type: ignore
        await event.answer(error_message)
        await self.return_to_main_menu(event, state)

    @staticmethod
    async def return_to_main_menu(event: 'Message', state: 'FSMContext') -> None:
        await state.clear()
        await event.answer(
            text='Попробуем начать заново 😊',
            reply_markup=get_initial_keyboard(event),
        )
