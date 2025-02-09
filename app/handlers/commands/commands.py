from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.actions import get_initial_keyboard

commands_router = Router(name=__name__)


@commands_router.message(Command('start'))
async def handle_cmd_start(message: Message, state: FSMContext):
    """Обработчик события команды /start"""

    await state.clear()
    await message.answer(
        text=f'Привет 🤝, {message.from_user.full_name}! Пожалуйста, выбери действие:',
        reply_markup=get_initial_keyboard(),
    )


@commands_router.message(Command('help'))
async def handle_cmd_help(message: Message):
    """Обработчик события команды /help"""

    help_text = (
        '<b>Доступные действия:</b>\n\n'
        '<b>1. Задать вопрос</b> — чтобы задать новый вопрос боту\n'
        '<b>2. Выйти</b> — чтобы выйти из текущего диалога\n'
        '<b>3. Получить картинку</b> — сгенерировать картинку (от 1 до 3) по запросу\n'
        'Активируй бота командной /start, чтобы продолжить!'
    )
    await message.answer(help_text)
