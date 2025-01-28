from aiogram import Dispatcher

from app.handlers.actions import action_router
from app.handlers.images import setup_image_routers
from app.handlers.others import other_router


def setup_routers(dp: Dispatcher) -> Dispatcher:
	dp.include_routers(
		action_router,
		other_router,
		setup_image_routers(),
	)
	return dp
