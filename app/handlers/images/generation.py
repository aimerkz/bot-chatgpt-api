from aiogram import Router, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from clients.openai import OpenAIClient
from config_reader import settings
from filters.type_message import TextFilter
from handlers.images import logic
from middlewares.exceptions import OpenAIExceptionMiddleware
from middlewares.openai_client import OpenAIMiddleware
from states.state import ImageState

generation_router = Router(name=__name__)

generation_router.message.middleware(
    OpenAIMiddleware(settings.api_key.get_secret_value())
)
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

    await logic.send_generated_image(
        message,
        image_count,
        openai_client,
        state,
    )
