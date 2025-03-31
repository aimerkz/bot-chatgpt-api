import os
from datetime import datetime
from typing import cast

import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage
from aiogram.types import Chat, Message, Update, User
from faker import Faker
from tests.integration_tests.mocked_bot import MockedBot

from handlers import setup_routers
from storage.factory import storage_factory

fake = Faker()


@pytest.fixture(scope='session', autouse=True)
async def storage():
    storage = storage_factory()
    yield storage
    await storage.close()


@pytest.fixture(scope='session', autouse=True)
async def bot():
    return MockedBot()


@pytest.fixture(scope='session', autouse=True)
async def dispatcher(storage, bot):
    dp = Dispatcher(storage=storage, bot=bot)
    setup_routers(dp)
    await dp.emit_startup()
    yield dp
    await dp.emit_shutdown()


@pytest.fixture
def user_factory() -> User:
    user = User(
        id=fake.random_int(1, 10),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_bot=False,
        username=fake.user_name(),
    )
    return user


@pytest.fixture
def chat_factory() -> Chat:
    chat = Chat(id=fake.random_int(1, 10), type='private')
    return chat


@pytest.fixture
def message_factory(user_factory, chat_factory):
    def factory(text: str) -> Message:
        return Message(
            message_id=fake.random_int(1, 10),
            from_user=user_factory,
            chat=chat_factory,
            text=text,
            date=datetime.now(),
        )

    return factory


@pytest.fixture
def update_factory():
    def factory(message: Message) -> Update:
        return Update(message=message, update_id=fake.random_int(1, 10))

    return factory


@pytest.fixture
def sent_message_factory(bot: MockedBot):
    def factory(message: Message, response_text: str) -> None:
        bot.add_result_for(
            SendMessage,
            ok=True,
            result=Message(
                message_id=message.message_id,
                chat=message.chat,
                text=response_text,
                date=datetime.now(),
            ),
        )

    return factory


@pytest.fixture(scope='session')
def admin_factory() -> User:
    admin = User(
        id=cast(int, os.getenv('ADMIN_ID')),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_bot=False,
        username=fake.user_name(),
    )
    return admin
