from aiogram import F, Router, flags
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from clients.openai import OpenAIClient
from keyboards.actions import get_exit_keyboard, get_initial_keyboard
from states.state import DialogState
from utils.enums import ActionsEnum

action_router = Router(name=__name__)


@action_router.message(Command('start'))
async def handle_start_command(message: Message, state: FSMContext):
    """Обработчик события команды /start"""

    await state.clear()
    await message.answer(
        text=f'Привет 🤝, {message.from_user.full_name}! Пожалуйста, выбери действие:',
        reply_markup=get_initial_keyboard(),
    )


@action_router.message(Command('help'))
async def cmd_help(message: Message):
    help_text = (
        '<b>Доступные действия:</b>\n\n'
        '<b>1. Задать вопрос</b> — чтобы задать новый вопрос боту\n'
        '<b>2. Выйти</b> — чтобы выйти из текущего диалога\n'
        '<b>3. Получить фото</b> — сгенерировать фото по запросу\n'
        '<b>4. Новый вопрос</b> — чтобы задать новый вопрос\n'
        '<b>5. Продолжить</b> — продолжить текущий диалог\n\n'
        'Активируй бота командной /start, чтобы продолжить!'
    )
    await message.answer(help_text)


@action_router.message(F.text == ActionsEnum.ASK.value)
async def handle_ask_question(message: Message, state: FSMContext):
    """Обработчик события по кнопке 'Задать вопрос'"""

    await message.answer(
        text='Отлично! Напиши свой вопрос, и я отправлю его ChatGPT',
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(DialogState.active)


@action_router.message(F.text == ActionsEnum.EXIT.value)
async def handle_handle_exit(message: Message, state: FSMContext):
    """Обработчик события по кнопке 'Выйти'"""

    await state.clear()
    await message.answer(
        text='До встречи 👋',
        reply_markup=ReplyKeyboardRemove(),
    )


@action_router.message(StateFilter(DialogState.active))
@flags.chat_action('typing')
async def handle_question_input(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient,
):
    """Обработчик события получения нового вопроса"""

    await message.answer('Отправил твой вопрос, ждем ответ ⌛')

    answer = await openai_client.ask(message.text, state)
    await state.update_data(last_response=answer)

    await message.reply(answer)

    await message.answer(
        text='Можешь задать новый вопрос или нажать <b>Выйти</b>, чтобы завершить диалог',
        reply_markup=get_exit_keyboard(),
    )
