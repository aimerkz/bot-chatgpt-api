import logging

from aiogram import Dispatcher

from app.config_reader import config
from app.middlewares.exceptions import OpenAIExceptionMiddleware
from app.middlewares.logs import LoggingMiddleware
from app.middlewares.openai import OpenAIMiddleware
from app.middlewares.typing import TypingMiddleware


def setup_middlewares(dp: Dispatcher) -> Dispatcher:
    logger = logging.getLogger('aiogram')

    dp.message.middleware(
        OpenAIMiddleware(config.api_key.get_secret_value()),
    )
    dp.message.middleware(LoggingMiddleware(logger))
    dp.message.middleware(TypingMiddleware())
    dp.message.middleware(OpenAIExceptionMiddleware())

    return dp
