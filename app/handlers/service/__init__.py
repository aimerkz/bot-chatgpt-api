from aiogram import Router

from handlers.service.service import service_router


def setup_service_routers() -> Router:
	router = Router()
	router.include_router(service_router)
	return router
