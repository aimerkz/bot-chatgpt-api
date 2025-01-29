from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from app.inlines.actions import get_continue_keyboard, get_initial_keyboard
from app.states.waiting import WaitingState

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


@other_router.message(Command('help'))
async def cmd_help(message: Message):
    help_text = (
        '<b>Доступные действия:</b>\n\n'
        '<b>1. Задать вопрос</b> — чтобы задать новый вопрос боту\n'
        '<b>2. Выйти</b> — чтобы выйти из текущего диалога\n'
        '<b>3. Получить фото</b> — сгенерировать фото по запросу\n'
        '<b>4. Новый вопрос</b> — чтобы задать новый вопрос\n'
        '<b>5. Продолжить</b> — продолжить текущий диалог\n\n'
        'Активируй бота командной /start, чтобы продолжить!'
    )
    await message.answer(help_text)
