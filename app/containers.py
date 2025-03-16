from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions
from dependency_injector import containers, providers

from config_reader import settings
from storage.storage import get_storage


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    bot = providers.Singleton(
        Bot,
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview=LinkPreviewOptions(
                is_disabled=False,
                prefer_small_media=True,
            ),
        ),
    )

    storage = providers.Singleton(get_storage)

    dp = providers.Singleton(
        Dispatcher,
        storage=storage,
        bot=bot,
    )
