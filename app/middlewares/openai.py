from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from openai import AsyncOpenAI

from app.clients.openai import OpenAIClient


class OpenAIMiddleware(BaseMiddleware):
	def __init__(self, api_key: str) -> None:
		self.client = OpenAIClient(
			AsyncOpenAI(api_key=api_key, base_url='https://api.openai.com/v1'),
		)

	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: TelegramObject,
		data: Dict[str, Any],
	):
		data['openai_client'] = self.client
		return await handler(event, data)
