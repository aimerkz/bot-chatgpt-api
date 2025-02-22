from typing import TYPE_CHECKING

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from config_reader import config
from utils.enums import BotEnvEnum

if TYPE_CHECKING:
    from aiogram.fsm.storage.base import BaseStorage


def get_storage() -> 'BaseStorage':
    match config.bot_env:
        case BotEnvEnum.DEV:
            return MemoryStorage()
        case BotEnvEnum.PROD:
            return RedisStorage.from_url(
                url=config.redis_dsn,
                connection_kwargs={'decode_responses': True},
            )
