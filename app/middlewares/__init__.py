from aiogram import Dispatcher

from middlewares.containers import MiddlewaresContainer


def setup_middlewares(dp: Dispatcher) -> Dispatcher:
    middlewares_container = MiddlewaresContainer()
    dp.update.middleware(middlewares_container.logging_middleware())
    dp.message.middleware(middlewares_container.throttling_middleware())
    dp.message.middleware(middlewares_container.chat_action_middleware())
    return dp
