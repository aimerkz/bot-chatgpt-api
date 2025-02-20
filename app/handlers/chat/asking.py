from aiogram import F, Router, flags, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from clients.openai import OpenAIClient
from config_reader import config
from filters.type_message import TextOrImageFilter
from keyboards.actions import get_exit_keyboard
from middlewares.exceptions import OpenAIExceptionMiddleware
from middlewares.openai_client import OpenAIMiddleware
from states.state import DialogState
from utils.enums import ActionsEnum, MessageTypeEnum
from utils.images import get_image_url

asking_router = Router(name=__name__)

asking_router.message.middleware(OpenAIMiddleware(config.api_key.get_secret_value()))
asking_router.message.middleware(OpenAIExceptionMiddleware())


@asking_router.message(F.text == ActionsEnum.ASK)
async def handle_ask_question(message: Message, state: FSMContext):
    """Обработчик события по кнопке 'Задать вопрос'"""

    await message.answer(
        text='Отлично! Напиши свой вопрос, и я отправлю его ChatGPT',
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(DialogState.active)


@asking_router.message(F.text == ActionsEnum.EXIT)
async def handle_handle_exit(message: Message, state: FSMContext):
    """Обработчик события по кнопке 'Выйти'"""

    await state.clear()
    await message.answer(
        text='До встречи 👋',
        reply_markup=ReplyKeyboardRemove(),
    )


@asking_router.message(
    StateFilter(DialogState.active),
    TextOrImageFilter(),
)
@flags.chat_action('typing')
async def handle_question_input(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient,
):
    """Обработчик события получения нового вопроса"""

    await message.answer(text='Отправил твой вопрос, ждем ответ ⌛')

    if message.text:
        answer = await openai_client.ask(
            user_text=message.text,
            state=state,
            type_message=MessageTypeEnum.TEXT,
        )

    else:
        image_url = await get_image_url(message)
        answer = await openai_client.ask(
            image_url=image_url,
            type_message=MessageTypeEnum.IMAGE_URL,
            state=state,
        )

    await state.update_data(last_response=answer)
    await message.reply(text=answer)

    await message.answer(
        text=f'Можешь задать новый вопрос или нажать {html.bold("Выйти")}, чтобы завершить диалог',
        reply_markup=get_exit_keyboard(),
    )
