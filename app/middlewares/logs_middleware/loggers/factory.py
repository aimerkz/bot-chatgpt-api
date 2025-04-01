from typing import TYPE_CHECKING

from middlewares.logs_middleware.loggers.dev import DevLogger
from middlewares.logs_middleware.loggers.prod import ProdLogger
from utils.enums import BotEnvEnum

if TYPE_CHECKING:
	from middlewares.logs_middleware.loggers.base import BaseLogger


class LoggerFactory:
	@staticmethod
	def get_logger(bot_env: BotEnvEnum = BotEnvEnum.DEV) -> 'BaseLogger':
		loggers = {
			BotEnvEnum.DEV: DevLogger,
			BotEnvEnum.PROD: ProdLogger,
		}
		return loggers[bot_env]()
