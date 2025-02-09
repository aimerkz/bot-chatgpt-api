from aiogram import Dispatcher

from handlers.chat import setup_asking_routers
from handlers.commands import setup_commands_routers
from handlers.images import setup_image_routers
from handlers.others import setup_service_routers


def setup_routers(dp: Dispatcher) -> Dispatcher:
    dp.include_routers(
        setup_commands_routers(),
        setup_asking_routers(),
        setup_image_routers(),
        setup_service_routers(),
    )
    return dp
