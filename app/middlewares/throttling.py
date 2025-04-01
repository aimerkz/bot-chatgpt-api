from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from cachetools import TTLCache

from utils.types import T


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = 1) -> None:
        self.limit = TTLCache(maxsize=1000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[T, Dict[str, Any]], Awaitable[Any]],
        event: T,
        data: Dict[str, Any],
    ) -> Any:
        user_id: int = event.from_user.id

        if user_id in self.limit:
            await event.answer('Слишком много сообщений 😓, попробуй через 1 сек')
            return

        self.limit[user_id] = None
        return await handler(event, data)
