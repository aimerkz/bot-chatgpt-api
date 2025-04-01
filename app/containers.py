from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions
from dependency_injector import containers, providers

from config_reader import settings
from storage.containers import StorageContainer


class BotInstanceContainer(containers.DeclarativeContainer):
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


class DispatcherContainer(containers.DeclarativeContainer):
    storage = providers.Container(StorageContainer)
    bot = providers.Container(BotInstanceContainer)
    dp = providers.Singleton(
        Dispatcher,
        storage=storage.storage_factory,
        bot=bot,
    )


class BotAppContainer(containers.DeclarativeContainer):
    bot = providers.Container(BotInstanceContainer)
    dp = providers.Container(DispatcherContainer)
