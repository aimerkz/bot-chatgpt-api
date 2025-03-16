from aiogram import Bot, Dispatcher
from dependency_injector.wiring import Provide, inject

from config_reader import settings
from containers import Container
from handlers import setup_routers
from middlewares import setup_middlewares
from utils.set_commands import set_default_commands


@inject
async def main(
    bot: Bot = Provide[Container.bot],
    dp: Dispatcher = Provide[Container.dp],
) -> None:
    setup_routers(dp)
    setup_middlewares(dp)

    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    from contextlib import suppress

    container = Container()
    container.wire(modules=[__name__])

    with suppress(KeyboardInterrupt):
        asyncio.run(main(), debug=settings.debug_mode)
