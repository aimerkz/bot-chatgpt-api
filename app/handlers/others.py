from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from keyboards.actions import get_initial_keyboard

other_router = Router(name=__name__)


@other_router.message(StateFilter(None))
async def handle_unexpected_input(message: Message):
    await message.reply(
        text='Сначала выбери действие с помощью кнопок 👇',
        reply_markup=get_initial_keyboard(),
    )
