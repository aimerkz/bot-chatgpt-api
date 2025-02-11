from aiogram import Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import LinkPreviewOptions, Message

from keyboards.actions import get_initial_keyboard

commands_router = Router(name=__name__)


@commands_router.message(Command('start'))
async def handle_cmd_start(message: Message, state: FSMContext):
    """Обработчик события команды /start"""

    await state.clear()
    await message.answer(
        text=f'Привет 🤝, {html.bold(message.from_user.full_name)}! Пожалуйста, выбери действие:',
        reply_markup=get_initial_keyboard(),
    )


@commands_router.message(Command('help'))
async def handle_cmd_help(message: Message):
    """Обработчик события команды /help"""

    help_text = (
        f'{html.italic(html.bold("Доступные действия:"))}\n\n'
        f'{html.bold("1. Задать вопрос")} — чтобы задать новый вопрос боту (текст или загрузка фото)\n\n'
        f'{html.bold("2. Выйти")} — чтобы выйти из текущего диалога\n\n'
        f'{html.bold("3. Получить картинку")} — сгенерировать картинку (от 1 до 3) по запросу\n\n'
        f'{html.bold("Активируй бота командной /start, чтобы продолжить!")}\n\n'
        f'{html.spoiler(html.link("Код бота на GitHub", "https://github.com/aimerkz/bot-chatgpt-api"))}'
    )
    await message.answer(
        help_text,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True,
            prefer_small_media=True,
        ),
    )
