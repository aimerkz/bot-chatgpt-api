from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import LinkPreviewOptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.utils.scheduler import start_scheduler
from config_reader import config
from handlers import setup_routers
from middlewares import setup_middlewares
from utils.set_commands import set_default_commands

scheduler = AsyncIOScheduler()


async def on_startup():
    start_scheduler()


async def on_shutdown():
    scheduler.shutdown()


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

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
