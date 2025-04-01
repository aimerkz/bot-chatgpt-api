import os
from datetime import datetime
from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock

import pytest
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.methods import SendMessage
from aiogram.types import Chat, Message, PhotoSize, Story, Update, User, Voice
from faker import Faker
from openai import AsyncOpenAI
from tests.integration_tests.mocked_bot import MockedBot

from clients.openai import OpenAIClient
from handlers import setup_routers
from storage.factory import storage_factory

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest

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
async def async_openai_client(request: 'FixtureRequest') -> AsyncOpenAI:
    strict = getattr(request, 'param', True)
    if not isinstance(strict, bool):
        raise TypeError(
            f'Unexpected fixture parameter type {type(strict)}, expected {bool}'
        )

    async with AsyncOpenAI(
        base_url='http://127.0.0.1:4010',
        api_key=os.getenv('API_KEY'),
        _strict_response_validation=strict,
    ) as client:
        return client


@pytest.fixture(scope='session')
async def openai_client(async_openai_client) -> OpenAIClient:
    client = OpenAIClient(client=async_openai_client)
    return client


@pytest.fixture
def mock_openai(mocker, openai_client) -> OpenAIClient:
    mocker.patch.object(
        openai_client,
        'ask',
        new_callable=AsyncMock,
        return_value='mock_response',
    )

    mocker.patch.object(
        openai_client,
        'convert_voice_to_text',
        new_callable=AsyncMock,
        return_value='mock_response',
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
def photo_size() -> list[PhotoSize]:
    return [
        PhotoSize(
            file_id=fake.pystr(1, 5),
            file_size=fake.random_int(100, 1000),
            file_unique_id=fake.pystr(1, 5),
            width=fake.random_int(500, 1000),
            height=fake.random_int(500, 1000),
        )
    ]


@pytest.fixture
def voice() -> Voice:
    return Voice(
        file_id=fake.pystr(1, 5),
        file_size=fake.random_int(100, 1000),
        file_unique_id=fake.pystr(1, 5),
        duration=fake.random_int(2, 5),
    )


@pytest.fixture
def story(chat_factory) -> Story:
    return Story(
        chat=chat_factory,
        id=fake.random_int(1, 10),
    )


@pytest.fixture(autouse=True)
async def mock_image_url(mocker):
    return mocker.patch(
        'handlers.chat.logic.get_image_url',
        new_callable=AsyncMock,
        return_value='https://127.0.0.1/image',
    )


@pytest.fixture(autouse=True)
async def mock_download_voice_file(mocker):
    return mocker.patch(
        'handlers.chat.logic.download_voice_file',
        new_callable=AsyncMock,
        return_value='/voices_dir/',
    )


@pytest.fixture
def message_factory(user_factory, chat_factory, photo_size, voice):
    def factory(
        text: str | None = None, is_photo: bool = False, is_voice: bool = False
    ) -> Message:
        return Message(
            message_id=fake.random_int(1, 10),
            from_user=user_factory,
            chat=chat_factory,
            text=text,
            date=datetime.now(),
            photo=photo_size if is_photo else None,
            voice=voice if is_voice else None,
        )

    return factory


@pytest.fixture
def incorrect_message(user_factory, chat_factory, story):
    return Message(
        message_id=fake.random_int(1, 10),
        from_user=user_factory,
        chat=chat_factory,
        date=datetime.now(),
        story=story,
    )


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
