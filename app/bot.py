from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import LinkPreviewOptions

from app.config_reader import config
from app.handlers import setup_routers
from app.middlewares import setup_middlewares
from app.utils.set_commands import set_default_commands


async def main():
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

    dp = Dispatcher(storage=MemoryStorage())
    setup_routers(dp)
    setup_middlewares(dp)

    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
