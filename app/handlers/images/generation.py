from aiogram import Router, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message

from clients.openai import OpenAIClient
from inlines.actions import get_base_keyboard, get_keyboard_after_get_images
from states.waiting import WaitingState
from utils.images import generate_images

generation_router = Router(name=__name__)


@generation_router.message(StateFilter(WaitingState.waiting_for_image_prompt))
@flags.chat_action('upload_photo')
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
        reply_markup=get_base_keyboard(),
    )

    await state.set_state(WaitingState.waiting_for_button)
    await send_generated_image(
        message,
        image_count,
        openai_client,
        state,
    )


async def send_generated_image(
    message: Message,
    image_count: int,
    openai_client: OpenAIClient,
    state: FSMContext,
):
    """Генерация изображения в фоне и отправка результата пользователю"""

    image_urls = await generate_images(message.text, image_count, openai_client)
    media_group = [InputMediaPhoto(media=url) for url in image_urls]

    await message.bot.send_media_group(
        chat_id=message.from_user.id,
        media=media_group,
    )

    await state.set_state(WaitingState.waiting_for_button)
    await message.answer(
        text='Что делаем дальше?',
        reply_markup=get_keyboard_after_get_images(),
    )
