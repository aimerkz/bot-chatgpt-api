import asyncio
from functools import wraps
from typing import Callable

from openai import OpenAIError


def retry_to_gpt_api(
    max_attempts: int = 3,
    delay: int = 2,
    backoff: int = 2,
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempts = 0

            while attempts < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except OpenAIError as error:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise error

                    wait_time = delay * (backoff ** (attempts - 1))
                    await asyncio.sleep(wait_time)

        return wrapper

    return decorator
