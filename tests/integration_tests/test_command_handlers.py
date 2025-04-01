import pytest
from aiogram.methods import SendMessage
from tests.integration_tests.conftest import admin_factory, user_factory

from utils.constants import help_text


@pytest.mark.asyncio
@pytest.mark.parametrize('user', (user_factory, admin_factory))
async def test_handle_cmd_start(
	bot, dispatcher, message_factory, update_factory, sent_message_factory, user
):
	message = message_factory('/start')
	update = update_factory(message)
	sent_message_factory(
		message,
		f'Привет 🤝, <b>{message.from_user.full_name}</b>! Пожалуйста, выбери действие:',
	)

	await dispatcher.feed_update(bot, update)
	request = bot.get_request()

	assert isinstance(request, SendMessage)
	assert (
		request.text
		== f'Привет 🤝, <b>{message.from_user.full_name}</b>! Пожалуйста, выбери действие:'
	)
	assert request.chat_id == message.chat.id
	assert len(request.reply_markup.keyboard[0]) >= 3


@pytest.mark.asyncio
async def test_handle_cmd_help(
	bot,
	dispatcher,
	message_factory,
	update_factory,
	sent_message_factory,
):
	message = message_factory('/help')
	update = update_factory(message)
	sent_message_factory(message, help_text)

	await dispatcher.feed_update(bot, update)
	request = bot.get_request()

	assert isinstance(request, SendMessage)
	assert request.text == help_text
	assert request.chat_id == message.chat.id
	assert request.reply_markup is None
