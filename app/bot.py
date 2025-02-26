from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions

from config_reader import config
from handlers import setup_routers
from middlewares import setup_middlewares
from storage.storage import get_storage
from utils.set_commands import set_default_commands


async def main() -> None:
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview=LinkPreviewOptions(
                is_disabled=False,
                prefer_small_media=True,
            ),
        ),
    )

    storage = get_storage()

    dp = Dispatcher(storage=storage, bot=bot)
    setup_routers(dp)
    setup_middlewares(dp)

    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    from contextlib import suppress

    with suppress(KeyboardInterrupt):
        asyncio.run(main(), debug=config.debug_mode)
