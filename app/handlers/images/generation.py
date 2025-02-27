from aiogram import Router, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message, ReplyKeyboardRemove

from clients.openai import OpenAIClient
from config_reader import config
from filters.type_message import TextFilter
from keyboards.actions import get_initial_keyboard
from middlewares.exceptions import OpenAIExceptionMiddleware
from middlewares.openai_client import OpenAIMiddleware
from states.state import ImageState
from utils.images import generate_images

generation_router = Router(name=__name__)

generation_router.message.middleware(OpenAIMiddleware(config.api_key.get_secret_value()))
generation_router.message.middleware(OpenAIExceptionMiddleware())


@generation_router.message(
    StateFilter(ImageState.to_generate),
    TextFilter(),
)
@flags.chat_action('upload_photo')
async def handle_image_prompt(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient,
):
    """Обрабатчик события ввода описания изображения"""

    data = await state.get_data()
    image_count = data.pop('image_count', 1)

    await message.answer(
        text='Пришлю, как будет готово',
        reply_markup=ReplyKeyboardRemove(),
    )

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

    await state.clear()
    await message.answer(
        text='Что делаем дальше?',
        reply_markup=get_initial_keyboard(message),
    )
