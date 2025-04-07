from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from aiogram.types import Message, PhotoSize, Story, Voice
from faker import Faker

fake = Faker()


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
def photo_message_factory(base_message_factory, photo_size):
    def factory() -> Message:
        msg = base_message_factory(photo_size=photo_size)
        return msg

    return factory


@pytest.fixture
def voice_message_factory(base_message_factory, voice):
    def factory() -> Message:
        msg = base_message_factory(voice=voice)
        return msg

    return factory
