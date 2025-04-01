from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware

if TYPE_CHECKING:
	from aiogram.types import TelegramObject

	from clients.openai import OpenAIClient


class OpenAIMiddleware(BaseMiddleware):
	def __init__(self, openai_client: 'OpenAIClient') -> None:
		self.client = openai_client

	async def __call__(
		self,
		handler: Callable[['TelegramObject', Dict[str, Any]], Awaitable[Any]],
		event: 'TelegramObject',
		data: Dict[str, Any],
	):
		data['openai_client'] = self.client
		return await handler(event, data)
