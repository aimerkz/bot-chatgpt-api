from aiogram import Bot, Dispatcher
from dependency_injector.wiring import Provide, inject

from config_reader import settings
from containers import BotAppContainer
from handlers import setup_routers
from middlewares import setup_middlewares
from utils.set_commands import set_default_commands


@inject
async def main(
	bot: Bot = Provide[BotAppContainer.bot.bot],
	dp: Dispatcher = Provide[BotAppContainer.dp.dp],
) -> None:
	setup_routers(dp)
	setup_middlewares(dp)

	await set_default_commands(bot)
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	import asyncio
	from contextlib import suppress

	container = BotAppContainer()
	container.wire(modules=[__name__])

	with suppress(KeyboardInterrupt):
		asyncio.run(main(), debug=settings.debug_mode)
