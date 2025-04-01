from aiogram import Router

from handlers.commands.commands import commands_router


def setup_commands_routers() -> Router:
	router = Router()
	router.include_router(commands_router)
	return router
