from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.state import ImageState
from utils.enums import ActionsEnum

image_router = Router(name=__name__)


@image_router.message(F.text == ActionsEnum.GENERATE_IMAGE)
async def handle_generate_image(message: Message, state: FSMContext):
    """Обработчик ввода числа генерируемых картинок"""

    await state.clear()
    await message.answer(
        text='Сколько картинок хочешь сгенерировать? (Число от 1 до 3)',
    )
    await state.set_state(ImageState.count_images)


@image_router.message(StateFilter(ImageState.count_images))
async def handle_image_count(message: Message, state: FSMContext):
    """Обработчик ввода описания генерируемых картинок"""

    try:
        count = int(message.text)
        if 1 <= count <= 3:
            await state.update_data(image_count=count)
            await message.answer(text='Опиши, какую картинку нужно сгенерировать')
            await state.set_state(ImageState.to_generate)
        else:
            await message.answer(text='Введи число от 1 до 3 😠')
    except (TypeError, ValueError):
        await message.answer(text='Введи число от 1 до 3 😠')
