from typing import TYPE_CHECKING, assert_never

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from config_reader import settings
from utils.enums import BotEnvEnum

if TYPE_CHECKING:
    from aiogram.fsm.storage.base import BaseStorage


def storage_factory() -> 'BaseStorage':
    match settings.bot_env:
        case BotEnvEnum.DEV:
            return MemoryStorage()
        case BotEnvEnum.PROD:
            return RedisStorage.from_url(
                url=settings.redis_dsn,
                connection_kwargs={'decode_responses': True},
            )
        case _:
            assert_never(settings.bot_env)
