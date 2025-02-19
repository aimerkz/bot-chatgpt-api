from unittest.mock import AsyncMock

import pytest
from aiogram.types import Chat, Message, User


@pytest.fixture(scope='session')
def fake_user():
    return User(
        id=123456, is_bot=False, first_name='Test', last_name='Testov', username='test'
    )


@pytest.fixture(scope='session')
def fake_admin():
    return User(
        id=666, is_bot=False, first_name='Admin', last_name='Adminov', username='admin'
    )


@pytest.fixture(scope='function')
def fake_message(fake_user):
    message = AsyncMock(spec=Message)
    message.from_user = fake_user
    message.chat = Chat(id=fake_user.id, type='private')
    message.answer = AsyncMock()
    message.reply = AsyncMock()
    return message


@pytest.fixture(scope='function')
def fake_message_for_admin(fake_admin):
    message = AsyncMock(spec=Message)
    message.from_user = fake_admin
    message.chat = Chat(id=fake_admin.id, type='private')
    message.answer = AsyncMock()
    message.reply = AsyncMock()
    return message
