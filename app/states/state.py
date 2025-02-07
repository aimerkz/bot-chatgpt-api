from aiogram.fsm.state import State, StatesGroup


class DialogState(StatesGroup):
    active = State()


class ImageState(StatesGroup):
    count_images = State()
    to_generate = State()
