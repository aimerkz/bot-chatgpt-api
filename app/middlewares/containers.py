from aiogram.utils.chat_action import ChatActionMiddleware
from dependency_injector import containers, providers
from openai import AsyncOpenAI

from clients.openai import OpenAIClient
from config_reader import settings
from middlewares.exceptions import OpenAIExceptionMiddleware
from middlewares.logs_middleware.loggers.containers import LoggerContainer
from middlewares.logs_middleware.main_middleware import LoggingMiddleware
from middlewares.openai_client import OpenAIMiddleware
from middlewares.state_cleaner import DeferredClearStateMiddleware
from middlewares.throttling import ThrottlingMiddleware


class MiddlewaresContainer(containers.DeclarativeContainer):
    logger_container = providers.Container(LoggerContainer)
    logging_middleware = providers.Singleton(
        LoggingMiddleware, logger=logger_container.logger
    )

    throttling_middleware = providers.Singleton(ThrottlingMiddleware)
    chat_action_middleware = providers.Singleton(ChatActionMiddleware)
    state_cleaner_middleware = providers.Singleton(DeferredClearStateMiddleware)

    openai_client = providers.Singleton(
        OpenAIClient,
        client=providers.Object(
            AsyncOpenAI(
                api_key=settings.api_key.get_secret_value(),
                base_url='https://api.openai.com/v1',
            ),
        ),
    )
    openai_middleware = providers.Singleton(
        OpenAIMiddleware,
        openai_client=openai_client,
    )

    openai_exception_middleware = providers.Singleton(
        OpenAIExceptionMiddleware,
    )
