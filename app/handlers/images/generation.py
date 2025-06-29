from aiogram import Router, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from clients.openai import OpenAIClient
from filters.type_message import TextFilter
from handlers.images import logic
from keyboards.actions import get_initial_keyboard
from states.state import ImageState

generation_router = Router(name=__name__)


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
        text='Пришлю\\, как будет готово',
        reply_markup=get_initial_keyboard(message),
    )

    await logic.send_generated_image(
        message,
        image_count,
        openai_client,
        state,
    )
