import os
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.methods import SendMessage
from aiogram.types import Chat, Message, PhotoSize, Update, User, Voice
from faker import Faker
from openai import AsyncOpenAI

from clients.openai import OpenAIClient
from handlers import setup_routers
from storage.factory import storage_factory
from tests.integration_tests.mocked_bot import MockedBot

fake = Faker()


@pytest.fixture(scope='session', autouse=True)
async def storage():
    storage = storage_factory()
    yield storage
    await storage.close()


@pytest.fixture(scope='session')
async def bot():
    yield MockedBot()


@pytest.fixture(autouse=True)
async def clean_bot_requests_history(bot):
    bot.clean_history()


@pytest.fixture(scope='session', autouse=True)
async def dispatcher(storage, bot):
    dp = Dispatcher(storage=storage, bot=bot)
    setup_routers(dp)
    await dp.emit_startup()
    yield dp
    await dp.emit_shutdown()


@pytest.fixture
async def fsm_context_factory(bot, storage):
    async def factory(chat_id: int, user_id: int) -> FSMContext:
        key = StorageKey(
            chat_id=chat_id,
            user_id=user_id,
            bot_id=bot.id,
        )
        context = FSMContext(storage=storage, key=key)
        return context

    return factory


@pytest.fixture(scope='session')
async def async_openai_client() -> AsyncOpenAI:
    async with AsyncOpenAI(
        base_url='http://127.0.0.1:4010',
        api_key=os.getenv('API_KEY'),
    ) as client:
        yield client


@pytest.fixture(scope='session')
async def openai_client(async_openai_client) -> OpenAIClient:
    client = OpenAIClient(client=async_openai_client)
    yield client


@pytest.fixture
def mock_openai(mocker, openai_client) -> OpenAIClient:
    mocker.patch.object(
        openai_client,
        'ask',
        new_callable=AsyncMock,
        return_value='response',
    )

    mocker.patch.object(
        openai_client,
        'convert_voice_to_text',
        new_callable=AsyncMock,
        return_value='response',
    )

    return openai_client


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
def base_message_factory(user_factory, chat_factory):
    def factory(
        text: str | None = None,
        photo_size: PhotoSize | None = None,
        voice: Voice | None = None,
    ) -> Message:
        return Message(
            message_id=fake.random_int(1, 10),
            from_user=user_factory,
            chat=chat_factory,
            text=text,
            photo=photo_size,
            voice=voice,
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
    def factory(message: Message, *responses: str) -> None:
        for i, response in enumerate(responses, start=1):
            bot.add_result_for(
                SendMessage,
                ok=True,
                result=Message(
                    message_id=message.message_id + i,
                    chat=message.chat,
                    text=response,
                    date=datetime.now(),
                ),
            )

    return factory
