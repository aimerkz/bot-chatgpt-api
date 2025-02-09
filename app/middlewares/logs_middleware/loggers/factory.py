from middlewares.logs_middleware.loggers.base import BaseLogger
from middlewares.logs_middleware.loggers.dev import DevLogger
from middlewares.logs_middleware.loggers.prod import ProdLogger
from utils.enums import BotEnvEnum


class LoggerFactory:
    @staticmethod
    def get_logger(bot_env: BotEnvEnum) -> BaseLogger:
        loggers = {
            BotEnvEnum.DEV: DevLogger,
            BotEnvEnum.PROD: ProdLogger,
        }
        return loggers[bot_env]()
