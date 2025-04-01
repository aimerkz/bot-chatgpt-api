from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.users import IsAdminUser
from keyboards.actions import get_initial_keyboard
from keyboards.admin import get_admin_control_keyboard
from states.state import BotManagementState
from utils.enums import ActionsEnum, BotStatusEnum

service_router = Router(name=__name__)


@service_router.message(
	IsAdminUser(),
	F.text == ActionsEnum.BOT_MANAGEMENT,
)
async def handle_maintenance_on(message: Message):
	await message.answer(
		text='Выбери действие:',
		reply_markup=get_admin_control_keyboard(),
	)


@service_router.message(
	IsAdminUser(),
	F.text == BotStatusEnum.ON,
)
async def handle_activate_bot(message: Message, state: FSMContext):
	current_state = await state.get_state()

	if current_state is None:
		await message.answer(
			text='Бот уже активирован!',
			reply_markup=get_initial_keyboard(message),
		)
	else:
		await state.clear()
		await message.answer(
			text='Бот активирован!',
			reply_markup=get_initial_keyboard(message),
		)


@service_router.message(
	IsAdminUser(),
	F.text == BotStatusEnum.MAINTENANCE,
)
async def handle_maintenance_bot(message: Message, state: FSMContext):
	await state.clear()
	await state.set_state(BotManagementState.manage)
	await message.answer(
		text='Бот переведен в режим обслуживания',
		reply_markup=get_initial_keyboard(message),
	)


@service_router.message(StateFilter(BotManagementState.manage))
async def handle_manage_mod(message: Message):
	await message.answer(
		text='Бот находится на обслуживании, попробуй позже',
		reply_markup=get_initial_keyboard(message),
	)
