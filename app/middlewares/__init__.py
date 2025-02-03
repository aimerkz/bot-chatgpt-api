import logging

from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware

from config_reader import config
from middlewares.exceptions import OpenAIExceptionMiddleware
from middlewares.logs import LoggingMiddleware
from middlewares.openai import OpenAIMiddleware
from middlewares.throttling import ThrottlingMiddleware


def setup_middlewares(dp: Dispatcher) -> Dispatcher:
    logger = logging.getLogger('aiogram')

    dp.message.middleware(
        OpenAIMiddleware(config.api_key.get_secret_value()),
    )
    dp.message.middleware(LoggingMiddleware(logger))
    dp.message.middleware(OpenAIExceptionMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(ChatActionMiddleware())

    return dp
