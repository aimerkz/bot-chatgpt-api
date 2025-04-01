from unittest.mock import call

from aiogram import html

from keyboards.actions import get_exit_keyboard


def assert_common_calls(mock_message, mock_fsm, expected_response):
	mock_fsm.update_data.assert_called_once_with(last_response=expected_response)

	expected_calls = [
		call(text='Отправил твой вопрос, ждем ответ ⌛'),
		call(
			text=f'Можешь задать новый вопрос или нажать {html.bold("Выйти")}, чтобы завершить диалог',
			reply_markup=get_exit_keyboard(),
		),
	]
	mock_message.answer.assert_has_calls(expected_calls, any_order=False)
	mock_message.reply.assert_called_once_with(text=expected_response)
