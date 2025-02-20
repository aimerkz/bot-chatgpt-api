import pytest

from handlers.others.state_check import handle_unexpected_input
from keyboards.actions import get_initial_keyboard


@pytest.mark.asyncio
async def test_others_handler(mock_message):
    await handle_unexpected_input(mock_message)
    mock_message.reply.assert_called_once_with(
        text='Сначала выбери действие с помощью кнопок 👇',
        reply_markup=get_initial_keyboard(mock_message),
    )
