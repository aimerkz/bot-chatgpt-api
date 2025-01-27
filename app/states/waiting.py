from aiogram.fsm.state import StatesGroup, State


class WaitingState(StatesGroup):
    waiting_for_question = State()
    waiting_for_button = State()
    waiting_for_image_prompt = State()
    waiting_for_image_count = State()
