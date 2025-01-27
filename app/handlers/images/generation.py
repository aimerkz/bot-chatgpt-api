import asyncio

from aiogram import Bot, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message

from app.clients.openai import OpenAIClient
from app.inlines.actions import get_initial_keyboard
from app.states.waiting import WaitingState
from app.utils.images import generate_images
from app.middlewares.throttling import ThrottlingMiddleware


generation_router = Router(name=__name__)
generation_router.message.middleware(ThrottlingMiddleware())


@generation_router.message(StateFilter(WaitingState.waiting_for_image_prompt))
async def handle_image_prompt(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient,
):
    """Обрабатчик события ввода описания изображения"""

    data = await state.get_data()
    image_count = data.get('image_count', 1)

    await message.answer(
        text='Пришлю, как будет готово',
        reply_markup=get_initial_keyboard(),
    )

    await state.set_state(WaitingState.waiting_for_button)
    asyncio.create_task(
        send_generated_image(
            message.from_user.id,
            message.text,
            image_count,
            message.bot,
            openai_client,
            state,
        )
    )


async def send_generated_image(
    user_id: int,
    description: str,
    image_count: int,
    bot: Bot,
    openai_client: OpenAIClient,
    state: FSMContext,
):
    """Генерация изображения в фоне и отправка результата пользователю"""

    image_urls = await generate_images(description, image_count, openai_client)
    media_group = [
        InputMediaPhoto(media=url) for url in image_urls
    ]

    await bot.send_media_group(
        chat_id=user_id,
        media=media_group,
    )

    await state.set_state(WaitingState.waiting_for_button)
