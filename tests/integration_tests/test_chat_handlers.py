import pytest
from aiogram import html
from aiogram.methods import SendMessage
from aiogram.types import ReplyKeyboardRemove
from tests.integration_tests.logic import check_state, set_state

from states.state import DialogState
from utils.enums import ActionsEnum


@pytest.mark.asyncio
async def test_handle_ask_question(
    bot,
    dispatcher,
    message_factory,
    update_factory,
    sent_message_factory,
    fsm_context_factory,
):
    message = message_factory(ActionsEnum.ASK)
    update = update_factory(message)
    sent_message_factory(message, 'Отлично! Напиши свой вопрос, и я отправлю его ChatGPT')

    await dispatcher.feed_update(bot, update)
    request = bot.get_request()
    assert isinstance(request, SendMessage)
    assert request.text == 'Отлично! Напиши свой вопрос, и я отправлю его ChatGPT'
    assert request.chat_id == message.chat.id
    assert isinstance(request.reply_markup, ReplyKeyboardRemove)
    await check_state(fsm_context_factory, message, DialogState.active)


@pytest.mark.asyncio
async def test_handle_exit(
    bot,
    dispatcher,
    message_factory,
    update_factory,
    sent_message_factory,
    fsm_context_factory,
):
    message = message_factory(ActionsEnum.EXIT)
    update = update_factory(message)
    sent_message_factory(message, 'До встречи 👋')

    await dispatcher.feed_update(bot, update)
    request = bot.get_request()
    assert isinstance(request, SendMessage)
    assert request.text == 'До встречи 👋'
    assert request.chat_id == message.chat.id
    assert isinstance(request.reply_markup, ReplyKeyboardRemove)
    await check_state(fsm_context_factory, message, None)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'content_type, content',
    [
        ('text', 'Test question'),
        ('is_photo', True),
        ('is_voice', True),
    ],
)
async def test_handle_question_input_text(
    bot,
    dispatcher,
    mock_openai,
    fsm_context_factory,
    message_factory,
    update_factory,
    sent_message_factory,
    content_type,
    content,
):
    message = message_factory(**{content_type: content})
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
    requests = bot.get_requests()
    last_response = await fsm.get_data()

    mock_openai.ask.assert_awaited_once()
    assert len(requests) == 3
    assert all(
        req.text == expected_response
        for req, expected_response in zip(requests, expected_responses)
    )
    assert last_response['last_response'] == mock_openai.ask.return_value
    assert len(requests[-1].reply_markup.keyboard[0]) == 1


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
    mock_openai.ask.assert_not_awaited()
