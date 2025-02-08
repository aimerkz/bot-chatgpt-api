from aiogram import Router

from handlers.chat.actions import action_router


def setup_chat_routers() -> Router:
    router = Router()
    router.include_router(action_router)
    return router
