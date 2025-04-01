from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from utils.enums import BotStatusEnum


def get_admin_control_keyboard() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text=BotStatusEnum.ON)],
			[KeyboardButton(text=BotStatusEnum.MAINTENANCE)],
		],
		resize_keyboard=True,
		one_time_keyboard=True,
	)
	return keyboard
