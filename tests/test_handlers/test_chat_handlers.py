from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest
from aiogram import html
from aiogram.types import ReplyKeyboardRemove

from handlers.chat.asking import (
    handle_ask_question,
    handle_handle_exit,
    handle_question_input,
)
from keyboards.actions import get_exit_keyboard
from states.state import DialogState
from utils.enums import MessageTypeEnum


@pytest.mark.asyncio
async def test_handle_ask_question(mock_message, mock_fsm):
    await handle_ask_question(mock_message, mock_fsm)
    mock_message.answer.assert_called_once_with(
        text='Отлично! Напиши свой вопрос, и я отправлю его ChatGPT',
        reply_markup=ReplyKeyboardRemove(),
    )
    mock_fsm.set_state.assert_called_once_with(DialogState.active)


@pytest.mark.asyncio
async def test_handle_handle_exit(mock_message, mock_fsm):
    await handle_handle_exit(mock_message, mock_fsm)
    mock_fsm.clear.assert_called_once()
    mock_message.answer.assert_called_once_with(
        text='До встречи 👋',
        reply_markup=ReplyKeyboardRemove(),
    )


@pytest.mark.asyncio
async def test_handle_question_text_input(mock_message, mock_fsm, mock_openai_client):
    mock_message.text = 'some image description'
    mock_openai_client.ask.return_value = 'some answer'

    await handle_question_input(mock_message, mock_fsm, mock_openai_client)

    mock_openai_client.ask.assert_called_once_with(
        user_text=mock_message.text,
        state=mock_fsm,
        type_message=MessageTypeEnum.TEXT,
    )
    mock_message.reply.assert_called_once_with(
        text=mock_openai_client.ask.return_value,
    )
    mock_fsm.update_data.assert_called_once_with(
        last_response=mock_openai_client.ask.return_value
    )

    expected_calls = [
        call(text='Отправил твой вопрос, ждем ответ ⌛'),
        call(
            text=f'Можешь задать новый вопрос или нажать {html.bold("Выйти")}, чтобы завершить диалог',
            reply_markup=get_exit_keyboard(),
        ),
    ]
    mock_message.answer.assert_has_calls(expected_calls, any_order=False)


@pytest.mark.asyncio
@patch('utils.images.get_image_url', new_callable=AsyncMock)
async def test_handle_question_image_input(
    mock_image_url, mock_message, mock_fsm, mock_openai_client
):
    mock_message.bot = AsyncMock()
    mock_message.bot.token = '/token'

    mock_file_info = AsyncMock()
    mock_file_info.file_path = 'path/to/file'
    mock_message.bot.get_file.return_value = mock_file_info

    mock_image_url.return_value = 'https://api.telegram.org/file/bot/token/path/to/file'

    mock_message.text = None
    mock_message.photo = MagicMock()

    mock_openai_client.ask.return_value = [MagicMock()]

    await handle_question_input(mock_message, mock_fsm, mock_openai_client)

    mock_openai_client.ask.assert_called_once_with(
        image_url='https://api.telegram.org/file/bot/token/path/to/file',
        state=mock_fsm,
        type_message=MessageTypeEnum.IMAGE_URL,
    )
    mock_fsm.update_data.assert_called_once_with(
        last_response=mock_openai_client.ask.return_value
    )

    expected_calls = [
        call(text='Отправил твой вопрос, ждем ответ ⌛'),
        call(
            text=f'Можешь задать новый вопрос или нажать {html.bold("Выйти")}, чтобы завершить диалог',
            reply_markup=get_exit_keyboard(),
        ),
    ]

    mock_message.answer.assert_has_calls(expected_calls, any_order=False)
    mock_message.reply.assert_called_once_with(text=mock_openai_client.ask.return_value)
