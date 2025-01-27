from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.clients.openai import OpenAIClient
from app.inlines.actions import get_initial_keyboard, get_continue_keyboard
from app.states.waiting import WaitingState
from app.utils.enums import ActionsEnum

action_router = Router(name=__name__)


@action_router.message(Command('start'))
async def handle_start_command(message: Message):
    """Обработчик события команды /start"""

    await message.answer(
        text=f'Привет 🤝, {message.from_user.full_name}! Пожалуйста, выбери действие:',
        reply_markup=get_initial_keyboard(),
    )


@action_router.callback_query(F.data == ActionsEnum.ASK)
async def handle_ask_question(callback: CallbackQuery, state: FSMContext):
    """Обработчик события по кнопке 'Задать вопрос'"""

    await callback.message.edit_text(
        text='Отлично! Напиши свой вопрос, и я отправлю его ChatGPT',
    )
    await state.set_state(WaitingState.waiting_for_question)


@action_router.callback_query(F.data == ActionsEnum.NEW_QUESTION)
async def handle_new_question(callback: CallbackQuery, state: FSMContext):
    """Обработчик события по кнопке 'Задать новый вопрос'"""

    await state.clear()
    await callback.message.edit_text(
        text='Отлично! Напиши новый вопрос',
    )
    await state.set_state(WaitingState.waiting_for_question)


@action_router.message(StateFilter(WaitingState.waiting_for_question))
async def handle_question_input(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient,
):
    """Обработчик события получения нового вопроса"""

    question = message.text
    await message.answer('Отправил твой вопрос, ждем ответ ⌛')

    answer = await openai_client.ask(question, state)
    await state.update_data(last_response=answer)

    await message.reply(answer)
    await state.set_state(WaitingState.waiting_for_button)
    await message.answer(
        text='Что будем делать дальше?',
        reply_markup=get_continue_keyboard(),
    )


@action_router.callback_query(F.data == ActionsEnum.ASK_AGAIN)
async def handle_continue_chat(callback: CallbackQuery, state: FSMContext):
    """Обработчик события по кнопке 'Продолжить общение'"""

    await callback.message.edit_text(
        text='Напиши свой следующий вопрос',
    )
    await state.set_state(WaitingState.waiting_for_question)


@action_router.callback_query(F.data == ActionsEnum.EXIT)
async def handle_handle_exit(query: CallbackQuery, state: FSMContext):
    """Обработчик события по кнопке 'Выйти'"""

    await query.message.edit_text(
        text='До встречи 👋',
    )
    await state.clear()
