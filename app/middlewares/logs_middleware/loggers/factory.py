from typing import TYPE_CHECKING

from middlewares.logs_middleware.loggers.dev import DevLogger
from middlewares.logs_middleware.loggers.prod import ProdLogger
from utils.enums import BotEnvEnum

if TYPE_CHECKING:
    from middlewares.logs_middleware.loggers.base import BaseLogger


class LoggerFactory:
    def __init__(self, bot_env: BotEnvEnum = BotEnvEnum.DEV) -> None:
        self.bot_env = bot_env

    def get_logger(self) -> 'BaseLogger':
        loggers = {
            BotEnvEnum.DEV: DevLogger,
            BotEnvEnum.PROD: ProdLogger,
        }
        return loggers[self.bot_env]()
