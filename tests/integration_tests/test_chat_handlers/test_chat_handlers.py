import pytest
from aiogram import html
from aiogram.types import ReplyKeyboardRemove

from states.state import DialogState
from tests.integration_tests.logic import check_state, set_state
from tests.integration_tests.test_chat_handlers.logic import assert_response
from utils.enums import ActionsEnum


@pytest.mark.asyncio
async def test_handle_ask_question(
    bot,
    dispatcher,
    base_message_factory,
    update_factory,
    sent_message_factory,
    fsm_context_factory,
):
    message = base_message_factory(ActionsEnum.ASK)
    update = update_factory(message)
    sent_message_factory(message, 'Отлично! Напиши свой вопрос, и я отправлю его ChatGPT')

    await dispatcher.feed_update(bot, update)
    request = bot.get_request()

    assert request.text == 'Отлично! Напиши свой вопрос, и я отправлю его ChatGPT'
    assert request.chat_id == message.chat.id
    assert isinstance(request.reply_markup, ReplyKeyboardRemove)
    await check_state(fsm_context_factory, message, DialogState.active)


@pytest.mark.asyncio
async def test_handle_exit(
    bot,
    dispatcher,
    base_message_factory,
    update_factory,
    sent_message_factory,
    fsm_context_factory,
):
    message = base_message_factory(ActionsEnum.EXIT)
    update = update_factory(message)
    sent_message_factory(message, 'До встречи 👋')

    await dispatcher.feed_update(bot, update)
    request = bot.get_request()

    assert request.text == 'До встречи 👋'
    assert request.chat_id == message.chat.id
    assert isinstance(request.reply_markup, ReplyKeyboardRemove)
    await check_state(fsm_context_factory, message, None)


@pytest.mark.asyncio
async def test_handle_question_text_input(
    bot,
    dispatcher,
    mock_openai,
    fsm_context_factory,
    update_factory,
    sent_message_factory,
    base_message_factory,
):
    message = base_message_factory('test_text')
    update = update_factory(message)
    dispatcher['openai_client'] = mock_openai

    fsm = await set_state(fsm_context_factory, message, DialogState.active)
    expected_responses = [
        'Отправил твой вопрос, ждем ответ ⌛',
        mock_openai.ask.return_value,
        f'Можешь задать новый вопрос или нажать {html.bold("Выйти")}, чтобы завершить диалог',
    ]

    sent_message_factory(message, *expected_responses)

    await dispatcher.feed_update(bot, update)
    await assert_response(bot, fsm, mock_openai, message, expected_responses)


@pytest.mark.asyncio
async def test_handle_question_image_input(
    bot,
    dispatcher,
    mock_openai,
    fsm_context_factory,
    update_factory,
    sent_message_factory,
    photo_message_factory,
):
    message = photo_message_factory()
    update = update_factory(message)
    dispatcher['openai_client'] = mock_openai

    fsm = await set_state(fsm_context_factory, message, DialogState.active)
    expected_responses = [
        'Отправил твой вопрос, ждем ответ ⌛',
        mock_openai.ask.return_value,
        f'Можешь задать новый вопрос или нажать {html.bold("Выйти")}, чтобы завершить диалог',
    ]

    sent_message_factory(message, *expected_responses)

    await dispatcher.feed_update(bot, update)
    await assert_response(bot, fsm, mock_openai, message, expected_responses)


@pytest.mark.asyncio
async def test_handle_question_voice_input(
    bot,
    dispatcher,
    mock_openai,
    fsm_context_factory,
    update_factory,
    sent_message_factory,
    voice_message_factory,
):
    message = voice_message_factory()
    update = update_factory(message)
    dispatcher['openai_client'] = mock_openai

    fsm = await set_state(fsm_context_factory, message, DialogState.active)
    expected_responses = [
        'Отправил твой вопрос, ждем ответ ⌛',
        mock_openai.ask.return_value,
        f'Можешь задать новый вопрос или нажать {html.bold("Выйти")}, чтобы завершить диалог',
    ]

    sent_message_factory(message, *expected_responses)

    await dispatcher.feed_update(bot, update)
    await assert_response(bot, fsm, mock_openai, message, expected_responses)


@pytest.mark.asyncio
async def test_handle_question_incorrect_input(
    bot,
    dispatcher,
    incorrect_message,
    update_factory,
    sent_message_factory,
    fsm_context_factory,
    mock_openai,
):
    update = update_factory(incorrect_message)
    await set_state(fsm_context_factory, incorrect_message, DialogState.active)

    sent_message_factory(
        incorrect_message, 'Отправь текст, картинку или голосовое сообщение 😠'
    )
    await dispatcher.feed_update(bot, update)

    requests = bot.get_requests()
    assert len(requests) == 1
    assert requests[0].text == 'Отправь текст, картинку или голосовое сообщение 😠'
    assert requests[0].reply_markup is None
    assert requests[0].chat_id == incorrect_message.chat.id
    mock_openai.ask.assert_not_awaited()
