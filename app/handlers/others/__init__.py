from aiogram import Router

from handlers.others.state_check import other_router


def setup_others_routers() -> Router:
	router = Router()
	router.include_router(other_router)
	return router
