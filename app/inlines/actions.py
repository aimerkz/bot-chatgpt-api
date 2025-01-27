from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.enums import ActionsEnum


def get_initial_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Задать вопрос', callback_data=ActionsEnum.ASK),
                InlineKeyboardButton(text='Выйти', callback_data=ActionsEnum.EXIT),
                InlineKeyboardButton(text='Сгенерировать картинку', callback_data=ActionsEnum.GENERATE_IMAGE)
            ]
        ]
    )

def get_continue_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Задать новый вопрос', callback_data=ActionsEnum.NEW_QUESTION),
                InlineKeyboardButton(text='Продолжить общение', callback_data=ActionsEnum.ASK_AGAIN),
                InlineKeyboardButton(text='Выйти', callback_data=ActionsEnum.EXIT),
            ]
        ]
    )

