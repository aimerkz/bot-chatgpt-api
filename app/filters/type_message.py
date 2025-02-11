from typing import TYPE_CHECKING

from aiogram.filters import BaseFilter

if TYPE_CHECKING:
    from aiogram.types.message import Message


class TextFilter(BaseFilter):
    async def __call__(self, message: 'Message') -> bool:
        if not message.text:
            await message.reply('Подойдет только текст 😠')
            return False
        return True


class TextOrImageFilter(BaseFilter):
    async def __call__(self, message: 'Message') -> bool:
        if not (message.text or message.photo):
            await message.reply('Отправь либо текст, либо картинку 😠')
            return False
        return True
