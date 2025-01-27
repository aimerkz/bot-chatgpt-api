import time

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self,
        time_limit: int = 60,
        max_requests: int = 5,
    ) -> None:
        self.limit = TTLCache(maxsize=1000, ttl=time_limit)
        self.max_requests = max_requests

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ):
        if event.text.startswith('/generate_image'):
            user_id = event.from_user.id
            current_time = time.time()

            if user_id in self.limit:
                requests_times = self.limit[user_id]
                requests_times = [point for point in requests_times if current_time - point <= self.limit.ttl]

                if len(requests_times) >= self.max_requests:
                    remaining_time = self.limit.ttl - (current_time - requests_times[0])
                    await event.answer(f'Слишком много попыток создания картинок, попробуй через {remaining_time} секунд')
                    return

                requests_times.append(current_time)
                self.limit[user_id] = requests_times

            else:
                self.limit[user_id] = [current_time]

        return await handler(event, data)
