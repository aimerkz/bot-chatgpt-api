from dependency_injector import containers, providers

from config_reader import settings
from middlewares.logs_middleware.loggers.factory import LoggerFactory
from middlewares.logs_middleware.main_middleware import LoggingMiddleware


class LoggerContainer(containers.DeclarativeContainer):
    logger_factory = providers.Singleton(
        LoggerFactory,
        bot_env=settings.bot_env,
    )
    logger = providers.Singleton(
        LoggerFactory.get_logger,
        logger_factory,
    )


class LoggingMiddlewareContainer(containers.DeclarativeContainer):
    logger = providers.Container(LoggerContainer)
    middleware = providers.Singleton(LoggingMiddleware, logger=logger.logger)
