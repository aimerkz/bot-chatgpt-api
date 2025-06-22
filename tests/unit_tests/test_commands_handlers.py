import pytest
from aiogram.types import LinkPreviewOptions

from handlers.commands.commands import handle_cmd_help, handle_cmd_start
from keyboards.actions import get_initial_keyboard
from utils.constants import help_text


@pytest.mark.asyncio
async def test_handle_cmd_start(mock_message):
    await handle_cmd_start(mock_message)

    keyboard = get_initial_keyboard(mock_message)
    buttons = [button for row in keyboard.keyboard for button in row]
    assert len(buttons) == 3

    mock_message.answer.assert_called_once_with(
        text=f'Привет 🤝\\, *{mock_message.from_user.full_name}*\\! Пожалуйста\\, выбери действие\\:',
        reply_markup=get_initial_keyboard(mock_message),
    )


@pytest.mark.asyncio
async def test_handle_cmd_start_for_admin(mock_message_for_admin):
    await handle_cmd_start(mock_message_for_admin)

    keyboard = get_initial_keyboard(mock_message_for_admin)
    buttons = [button for row in keyboard.keyboard for button in row]
    assert len(buttons) == 4

    mock_message_for_admin.answer.assert_called_once_with(
        text=f'Привет 🤝\\, *{mock_message_for_admin.from_user.full_name}*\\! Пожалуйста\\, выбери действие\\:',
        reply_markup=get_initial_keyboard(mock_message_for_admin),
    )


@pytest.mark.asyncio
async def test_handle_cmd_help(mock_message):
    await handle_cmd_help(mock_message)
    mock_message.answer.assert_called_once_with(
        help_text,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True,
            prefer_small_media=True,
        ),
    )
