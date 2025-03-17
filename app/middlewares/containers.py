from aiogram.utils.chat_action import ChatActionMiddleware
from dependency_injector import containers, providers

from middlewares.logs_middleware.loggers.containers import LoggingMiddlewareContainer
from middlewares.throttling import ThrottlingMiddleware


class MiddlewaresContainer(containers.DeclarativeContainer):
    logging_middleware = providers.Singleton(LoggingMiddlewareContainer.middleware)
    throttling_middleware = providers.Singleton(ThrottlingMiddleware)
    chat_action_middleware = providers.Singleton(ChatActionMiddleware)
