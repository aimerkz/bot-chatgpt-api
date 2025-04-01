from dependency_injector import containers, providers

from config_reader import settings
from middlewares.logs_middleware.loggers.factory import LoggerFactory


class LoggerContainer(containers.DeclarativeContainer):
	logger = providers.Singleton(
		LoggerFactory.get_logger,
		bot_env=settings.bot_env,
	)
