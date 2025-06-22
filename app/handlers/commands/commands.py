from aiogram import Router
from aiogram.filters import Command
from aiogram.types import LinkPreviewOptions, Message

from keyboards.actions import get_initial_keyboard
from utils.constants import help_text

commands_router = Router(name=__name__)


@commands_router.message(Command('start'))
async def handle_cmd_start(message: Message):
    """Обработчик события команды /start"""

    await message.answer(
        text=f'Привет 🤝\\, *{message.from_user.full_name}*\\! Пожалуйста\\, выбери действие\\:',
        reply_markup=get_initial_keyboard(message),
    )


@commands_router.message(Command('help'))
async def handle_cmd_help(message: Message):
    """Обработчик события команды /help"""

    await message.answer(
        help_text,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True,
            prefer_small_media=True,
        ),
    )
