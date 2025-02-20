import pytest

from handlers.service.service import (
    handle_activate_bot,
    handle_maintenance_bot,
    handle_maintenance_on,
    handle_manage_mod,
)
from keyboards.actions import get_initial_keyboard
from keyboards.admin import get_admin_control_keyboard
from states.state import BotManagementState


@pytest.mark.asyncio
async def test_handle_maintenance_on(mock_message_for_admin):
    await handle_maintenance_on(mock_message_for_admin)
    mock_message_for_admin.answer.assert_called_once_with(
        text='Выбери действие:',
        reply_markup=get_admin_control_keyboard(),
    )


@pytest.mark.asyncio
async def test_handle_manage_mod(mock_message):
    await handle_manage_mod(mock_message)
    mock_message.answer.assert_called_once_with(
        text='Бот находится на обслуживании, попробуй позже',
        reply_markup=get_initial_keyboard(mock_message),
    )


@pytest.mark.asyncio
async def test_handle_activate_bot_already_active(mock_message_for_admin, mock_fsm):
    mock_fsm.get_state.return_value = None
    await handle_activate_bot(mock_message_for_admin, mock_fsm)
    mock_message_for_admin.answer.assert_called_once_with(
        text='Бот уже активирован!',
        reply_markup=get_initial_keyboard(mock_message_for_admin),
    )


@pytest.mark.asyncio
async def test_handle_activate_bot(mock_message_for_admin, mock_fsm):
    mock_fsm.get_state.return_value = 'state'
    await handle_activate_bot(mock_message_for_admin, mock_fsm)
    mock_fsm.clear.assert_called_once()
    mock_message_for_admin.answer.assert_called_once_with(
        text='Бот активирован!',
        reply_markup=get_initial_keyboard(mock_message_for_admin),
    )


@pytest.mark.asyncio
async def test_handle_maintenance_bot(mock_message_for_admin, mock_fsm):
    mock_fsm.set_state.return_value = BotManagementState.manage
    await handle_maintenance_bot(mock_message_for_admin, mock_fsm)
    mock_fsm.clear.assert_called_once()
    mock_fsm.set_state.assert_called_once_with(BotManagementState.manage)
    mock_message_for_admin.answer.assert_called_once_with(
        text='Бот переведен в режим обслуживания',
        reply_markup=get_initial_keyboard(mock_message_for_admin),
    )
