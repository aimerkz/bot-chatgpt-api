from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.integration_tests.mocked_bot import MockedBot


async def assert_response(
    bot: 'MockedBot',
    fsm,
    mock_openai,
    message,
    expected_responses: list[str],
):
    requests = bot.get_requests()
    last_response = await fsm.get_data()

    mock_openai.ask.assert_awaited_once()
    assert len(requests) == 3
    assert all(
        req.text == expected_response and req.chat_id == message.chat.id
        for req, expected_response in zip(requests, expected_responses)
    )
    assert last_response['last_response'] == mock_openai.ask.return_value
    assert len(requests[-1].reply_markup.keyboard[0]) == 1
