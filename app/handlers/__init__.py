from aiogram import Dispatcher

from handlers.actions import action_router
from handlers.images import setup_image_routers
from handlers.others import other_router


def setup_routers(dp: Dispatcher) -> Dispatcher:
    dp.include_routers(
        action_router,
        other_router,
        setup_image_routers(),
    )
    return dp
