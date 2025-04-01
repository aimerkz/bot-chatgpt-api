from aiogram.fsm.state import StatesGroup


async def set_state(fsm_context_factory, message, state_value: StatesGroup | None):
	fsm = await fsm_context_factory(message.chat.id, message.from_user.id)
	await fsm.set_state(state_value)
	return fsm


async def check_state(
	fsm_context_factory, message, target_state_value: StatesGroup | None
) -> None:
	fsm = await fsm_context_factory(message.chat.id, message.from_user.id)
	state = await fsm.get_state()

	if target_state_value is not None:
		assert state == target_state_value
	else:
		assert state is None


async def check_state_data(fsm, key: str, value) -> None:
	state_data = await fsm.get_data()
	assert state_data[key] == value
