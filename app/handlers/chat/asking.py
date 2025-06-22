from aiogram import F, Router, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from clients.openai import OpenAIClient
from filters.type_message import TextOrImageOrVoiceFilter
from handlers.chat import logic
from keyboards.actions import get_exit_keyboard
from states.state import DialogState
from utils.enums import ActionsEnum
from utils.text_formatter import TelegramMarkdownV2Formatter

asking_router = Router(name=__name__)


@asking_router.message(F.text == ActionsEnum.ASK)
async def handle_ask_question(message: Message, state: FSMContext):
    """Обработчик события по кнопке 'Задать вопрос'"""

    await message.answer(
        text='Отлично\\! Напиши свой вопрос\\, и я отправлю его ChatGPT',
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(DialogState.active)


@asking_router.message(F.text == ActionsEnum.EXIT)
async def handle_exit(message: Message, state: FSMContext):
    """Обработчик события по кнопке 'Выйти'"""

    await state.clear()
    await message.answer(
        text='До встречи 👋',
        reply_markup=ReplyKeyboardRemove(),
    )


@asking_router.message(
    StateFilter(DialogState.active),
    TextOrImageOrVoiceFilter(),
)
@flags.chat_action('typing')
async def handle_question_input(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient,
):
    """Обработчик события получения нового вопроса"""

    await message.answer(text='Отправил твой вопрос\\, ждем ответ ⌛')

    if message.text:
        answer = await logic.process_text_message(message, openai_client, state)
    elif message.photo:
        answer = await logic.process_image_message(message, openai_client, state)
    else:
        answer = await logic.process_voice_message(message, openai_client, state)

    formatted_answer = TelegramMarkdownV2Formatter.format_answer_simple(answer)

    await state.update_data(last_response=formatted_answer)
    await message.reply(text=formatted_answer)

    await message.answer(
        text='Можешь задать новый вопрос или нажать *Выйти*\\, чтобы завершить диалог',
        reply_markup=get_exit_keyboard(),
    )
