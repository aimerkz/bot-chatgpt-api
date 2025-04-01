from typing import TYPE_CHECKING

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config_reader import settings
from utils.enums import ActionsEnum

if TYPE_CHECKING:
	from aiogram.types.message import Message


def get_initial_keyboard(message: 'Message') -> ReplyKeyboardMarkup:
	keyboard = [
		[
			KeyboardButton(text=ActionsEnum.ASK),
			KeyboardButton(text=ActionsEnum.EXIT),
			KeyboardButton(text=ActionsEnum.GENERATE_IMAGE),
		],
	]

	if message.from_user.id == settings.admin_id:
		maintenance_button = KeyboardButton(text=ActionsEnum.BOT_MANAGEMENT)
		keyboard[0].append(maintenance_button)

	return ReplyKeyboardMarkup(
		keyboard=keyboard,
		resize_keyboard=True,
	)


def get_exit_keyboard() -> ReplyKeyboardMarkup:
	return ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text=ActionsEnum.EXIT),
			]
		],
		resize_keyboard=True,
	)
