from aiogram import Router

from handlers.chat.asking import asking_router


def setup_asking_routers() -> Router:
    router = Router()
    router.include_router(asking_router)
    return router
