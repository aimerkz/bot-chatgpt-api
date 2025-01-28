from aiogram import Router

from app.handlers.images.base import image_router
from app.handlers.images.generation import generation_router


def setup_image_routers() -> Router:
    router = Router()
    router.include_router(image_router)
    router.include_router(generation_router)
    return router
