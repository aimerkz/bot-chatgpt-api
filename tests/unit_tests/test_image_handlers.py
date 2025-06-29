from unittest.mock import AsyncMock, patch

import pytest
from aiogram.types import ReplyKeyboardRemove

from handlers.images.base import handle_generate_image, handle_image_count
from handlers.images.generation import handle_image_prompt
from states.state import ImageState


@pytest.mark.asyncio
async def test_handle_generate_image(mock_message, mock_fsm):
    await handle_generate_image(mock_message, mock_fsm)
    mock_fsm.clear.assert_called_once()
    mock_message.answer.assert_called_once_with(
        text='Сколько картинок хочешь сгенерировать\\? \\(Число от 1 до 3\\)',
    )
    mock_fsm.set_state.assert_called_once_with(ImageState.count_images)


@pytest.mark.asyncio
async def test_handle_image_count(mock_message, mock_fsm):
    mock_message.text = 3
    await handle_image_count(mock_message, mock_fsm)
    mock_fsm.update_data.assert_called_once_with(image_count=mock_message.text)
    mock_fsm.set_state.assert_called_once_with(ImageState.to_generate)


@pytest.mark.asyncio
@pytest.mark.parametrize('image_count', (15, '15'))
async def test_handle_image_count_incorrect(mock_message, mock_fsm, image_count):
    mock_message.text = image_count
    await handle_image_count(mock_message, mock_fsm)
    mock_message.answer.assert_called_once_with(text='Введи число от 1 до 3 😠')


@pytest.mark.asyncio
@patch('handlers.images.logic.send_generated_image', new_callable=AsyncMock)
async def test_handle_image_prompt(
    mock_send_generated_image, mock_message, mock_fsm, mock_openai_client
):
    mock_fsm.get_data.return_value = {'image_count': 2}
    await handle_image_prompt(mock_message, mock_fsm, mock_openai_client)
    mock_message.answer.assert_called_once_with(
        text='Пришлю\\, как будет готово',
        reply_markup=ReplyKeyboardRemove(),
    )
    mock_send_generated_image.assert_called_once_with(
        mock_message,
        2,
        mock_openai_client,
        mock_fsm,
    )
