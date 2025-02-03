from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from inlines.actions import get_continue_keyboard, get_initial_keyboard
from states.waiting import WaitingState

other_router = Router(name=__name__)


@other_router.message(StateFilter(WaitingState.waiting_for_button))
async def handle_unexpected_text(message: Message):
    """Обработчик попытки ввода текста до нажатия на кнопку"""

    await message.answer(
        text='Пожалуйста, выбери действие с помощью кнопок 👇',
        reply_markup=get_continue_keyboard(),
    )


@other_router.message(StateFilter(None))
async def handle_unexpected_message(message: Message):
    """Обработчик ввода текста в других состояниях или без состояния"""

    await message.answer(
        text='Пожалуйста, выбери действие с помощью кнопок 👇',
        reply_markup=get_initial_keyboard(),
    )
