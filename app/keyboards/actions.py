from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from utils.enums import ActionsEnum


def get_base_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ActionsEnum.ASK.value),
                KeyboardButton(text=ActionsEnum.EXIT.value),
            ]
        ],
        resize_keyboard=True,
    )


def get_initial_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ActionsEnum.ASK.value),
                KeyboardButton(text=ActionsEnum.EXIT.value),
                KeyboardButton(text=ActionsEnum.GENERATE_IMAGE.value),
            ]
        ],
        resize_keyboard=True,
    )


def get_keyboard_after_get_images() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ActionsEnum.ASK.value),
                KeyboardButton(text=ActionsEnum.GENERATE_IMAGE.value),
                KeyboardButton(text=ActionsEnum.EXIT.value),
            ]
        ],
        resize_keyboard=True,
    )


def get_exit_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ActionsEnum.EXIT.value),
            ]
        ],
        resize_keyboard=True,
    )
