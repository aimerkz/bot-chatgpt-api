from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.types import ReplyKeyboardRemove

from handlers.chat.asking import (
    handle_ask_question,
    handle_exit,
    handle_question_input,
)
from states.state import DialogState
from tests.unit_tests.logic import assert_common_calls
from utils.constants import DOWNLOAD_VOICE_FILES_DIR
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
async def test_handle_exit(mock_message, mock_fsm):
    await handle_exit(mock_message, mock_fsm)
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
    assert_common_calls(mock_message, mock_fsm, mock_openai_client.ask.return_value)


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
    assert_common_calls(mock_message, mock_fsm, mock_openai_client.ask.return_value)


@pytest.mark.asyncio
@patch(
    target='utils.voice_messages.download_voice_file',
    return_value=f'{DOWNLOAD_VOICE_FILES_DIR}/mock_file_id.ogg',
)
async def test_handle_question_voice_input(
    mock_path,
    mock_message,
    mock_fsm,
    mock_openai_client,
):
    mock_message.text, mock_message.photo = None, None
    mock_message.voice = MagicMock()
    mock_message.voice.file_id = 'mock_file_id'

    mock_message.bot.get_file = AsyncMock(return_value=mock_path)
    mock_message.bot.download_file = AsyncMock()

    mock_openai_client.convert_voice_to_text.return_value = 'some text by voice message'
    mock_openai_client.ask.return_value = 'some answer from chat gpt'

    await handle_question_input(mock_message, mock_fsm, mock_openai_client)

    mock_openai_client.convert_voice_to_text.assert_called_once_with(
        mock_path.return_value
    )
    mock_openai_client.ask.assert_called_once_with(
        state=mock_fsm,
        user_text=mock_openai_client.convert_voice_to_text.return_value,
        type_message=MessageTypeEnum.TEXT,
    )
    assert_common_calls(mock_message, mock_fsm, mock_openai_client.ask.return_value)
