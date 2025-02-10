from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware

from config_reader import config
from middlewares.logs_middleware.loggers.factory import LoggerFactory
from middlewares.logs_middleware.main_middleware import LoggingMiddleware
from middlewares.throttling import ThrottlingMiddleware


def setup_middlewares(dp: Dispatcher) -> Dispatcher:
    dp.update.middleware(
        LoggingMiddleware(
            LoggerFactory().get_logger(config.bot_env),
        ),
    )
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(ChatActionMiddleware())
    return dp
