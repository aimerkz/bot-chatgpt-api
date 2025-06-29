from typing import TYPE_CHECKING

from aiogram.types import InputMediaPhoto

from utils.images import generate_images

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types.message import Message

    from clients.openai import OpenAIClient


async def send_generated_image(
    message: 'Message',
    image_count: int,
    openai_client: 'OpenAIClient',
    state: 'FSMContext',
):
    """Генерация изображения в фоне и отправка результата пользователю"""

    image_urls = await generate_images(message.text, image_count, openai_client)
    media_group = [InputMediaPhoto(media=url) for url in image_urls]

    await message.bot.send_media_group(
        chat_id=message.from_user.id,
        media=media_group,
    )
    await state.update_data(generation_complete=True)
