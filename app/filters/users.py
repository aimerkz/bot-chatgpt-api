from typing import TYPE_CHECKING

from aiogram.filters import BaseFilter

from config_reader import settings

if TYPE_CHECKING:
    from aiogram.types.message import Message


class IsAdminUser(BaseFilter):
    async def __call__(self, message: 'Message') -> bool:
        return message.from_user.id == settings.admin_id
