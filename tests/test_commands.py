import pytest
from aiogram import html
from aiogram.types import LinkPreviewOptions
from app.handlers.commands.commands import handle_cmd_help, handle_cmd_start
from app.keyboards.actions import get_initial_keyboard
from app.utils.constants import help_text


@pytest.mark.asyncio
async def test_handle_cmd_start(fake_message):
    await handle_cmd_start(fake_message)

    keyboard = get_initial_keyboard(fake_message)
    buttons = [button for row in keyboard.keyboard for button in row]
    assert len(buttons) == 3

    fake_message.answer.assert_called_once_with(
        text=f'Привет 🤝, {html.bold(fake_message.from_user.full_name)}! Пожалуйста, выбери действие:',
        reply_markup=get_initial_keyboard(fake_message),
    )


@pytest.mark.asyncio
async def test_handle_cmd_start_for_admin(fake_message_for_admin):
    await handle_cmd_start(fake_message_for_admin)

    keyboard = get_initial_keyboard(fake_message_for_admin)
    maintenance_button = [button for row in keyboard.keyboard for button in row]
    assert len(maintenance_button) == 4

    fake_message_for_admin.answer.assert_called_once_with(
        text=f'Привет 🤝, {html.bold(fake_message_for_admin.from_user.full_name)}! Пожалуйста, выбери действие:',
        reply_markup=get_initial_keyboard(fake_message_for_admin),
    )


@pytest.mark.asyncio
async def test_handle_cmd_help(fake_message):
    await handle_cmd_help(fake_message)
    fake_message.answer.assert_called_once_with(
        help_text,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True,
            prefer_small_media=True,
        ),
    )
