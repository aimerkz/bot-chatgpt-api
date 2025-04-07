import os
from typing import cast

import pytest
from aiogram.types import User
from faker import Faker

fake = Faker()


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
