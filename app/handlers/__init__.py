from aiogram import Dispatcher

from handlers.chat import setup_chat_routers
from handlers.images import setup_image_routers
from handlers.others import setup_service_routers


def setup_routers(dp: Dispatcher) -> Dispatcher:
    dp.include_routers(
        setup_chat_routers(),
        setup_image_routers(),
        setup_service_routers(),
    )
    return dp
