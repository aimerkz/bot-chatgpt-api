import asyncio
from typing import TYPE_CHECKING

from clients.openai import OpenAIClient

if TYPE_CHECKING:
    from aiogram.types.message import Message


async def generate_images(
    description: str,
    image_count: int,
    openai_client: OpenAIClient,
):
    image_tasks = [
        asyncio.create_task(openai_client.generate_image(description, count))
        for count in range(1, image_count + 1)
    ]
    done, _ = await asyncio.wait(image_tasks, return_when=asyncio.FIRST_EXCEPTION)
    result = [url.result() for url in done]
    return result


async def get_image_url(message: 'Message') -> str:
    file_info = await message.bot.get_file(message.photo[-1].file_id)
    return f'https://api.telegram.org/file/bot{message.bot.token}/{file_info.file_path}'
