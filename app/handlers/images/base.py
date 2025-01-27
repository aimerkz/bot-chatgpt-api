from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.states.waiting import WaitingState
from app.utils.enums import ActionsEnum

image_router = Router(name=__name__)


@image_router.callback_query(F.data == ActionsEnum.GENERATE_IMAGE)
async def handle_generate_image(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Сколько картинок хочешь сгенерировать? (Число от 1 до 3)',
    )
    await state.set_state(WaitingState.waiting_for_image_count)


@image_router.message(StateFilter(WaitingState.waiting_for_image_count))
async def handle_image_count(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        if 1 <= count <= 3:
            await state.update_data(image_count=count)
            await message.answer(text='Опиши, какую картинку нужно сгенерировать')
            await state.set_state(WaitingState.waiting_for_image_prompt)
        else:
            await message.answer('Введи число от 1 до 3')
    except ValueError:
        await message.answer('Введи корректное число')
