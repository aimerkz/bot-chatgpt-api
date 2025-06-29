from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject


class DeferredClearStateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        state: FSMContext | None = data.get('state')
        if state is None:
            return await handler(event, data)

        state_data = await state.get_data()

        if state_data.get('generation_complete', False) is True:
            await state.clear()

        return await handler(event, data)
