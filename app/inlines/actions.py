from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.enums import ActionsEnum


def get_base_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Задать вопрос', callback_data=ActionsEnum.ASK),
                InlineKeyboardButton(text='Выйти', callback_data=ActionsEnum.EXIT),
            ]
        ],
    )


def get_initial_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Задать вопрос', callback_data=ActionsEnum.ASK),
                InlineKeyboardButton(text='Выйти', callback_data=ActionsEnum.EXIT),
                InlineKeyboardButton(
                    text='Получить фото', callback_data=ActionsEnum.GENERATE_IMAGE
                ),
            ]
        ],
    )


def get_continue_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Новый вопрос', callback_data=ActionsEnum.NEW_QUESTION
                ),
                InlineKeyboardButton(
                    text='Продолжить', callback_data=ActionsEnum.ASK_AGAIN
                ),
                InlineKeyboardButton(text='Выйти', callback_data=ActionsEnum.EXIT),
            ]
        ],
    )


def get_keyboard_after_get_images() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Задать вопрос', callback_data=ActionsEnum.ASK),
                InlineKeyboardButton(
                    text='Получить новое фото', callback_data=ActionsEnum.GENERATE_IMAGE
                ),
                InlineKeyboardButton(text='Выйти', callback_data=ActionsEnum.EXIT),
            ]
        ],
    )
