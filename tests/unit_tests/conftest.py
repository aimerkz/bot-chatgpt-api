from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User

from clients.openai import OpenAIClient


@pytest.fixture(scope='session')
def mock_user():
	return User(
		id=123456,
		is_bot=False,
		first_name='Test',
		last_name='Testov',
		username='test',
		language_code='ru-RU',
	)


@pytest.fixture(scope='session')
def mock_admin():
	return User(
		id=666,
		is_bot=False,
		first_name='Admin',
		last_name='Adminov',
		username='admin',
		language_code='ru-RU',
	)


@pytest.fixture(scope='function')
def mock_message(mock_user):
	message = AsyncMock(spec=Message)
	message.from_user = mock_user
	message.answer = AsyncMock()
	message.reply = AsyncMock()
	return message


@pytest.fixture(scope='function')
def mock_message_for_admin(mock_admin):
	message = AsyncMock(spec=Message)
	message.from_user = mock_admin
	message.answer = AsyncMock()
	message.reply = AsyncMock()
	return message


@pytest.fixture(scope='function')
def mock_fsm():
	return AsyncMock(spec=FSMContext)


@pytest.fixture(scope='function')
def mock_openai_client():
	client = AsyncMock(spec=OpenAIClient)
	return client
