import asyncio

from app.clients.openai import OpenAIClient


async def generate_images(
    description: str,
    image_count: int,
    openai_client: OpenAIClient,
):
    image_tasks = [
        asyncio.create_task(openai_client.generate_image(description, count))
        for count in range(1, image_count + 1)
    ]
    done, pending = await asyncio.wait(image_tasks, return_when=asyncio.FIRST_EXCEPTION)
    result = [url.result() for url in done]
    return result
