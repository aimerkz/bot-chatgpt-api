from asyncio import Semaphore
from typing import TYPE_CHECKING

import openai
from openai import AsyncOpenAI

from app.exceptions.openai import (
	BadRequestOIException,
	NotFoundOIException,
	PermissionOIException,
	RateLimitImageOIException,
)

if TYPE_CHECKING:
	from aiogram.fsm.context import FSMContext


class OpenAIClient:
	max_history_length: int = 10
	model: str = 'gpt-4o-mini'
	semaphore: Semaphore
	max_requests_to_image: int = 5

	def __init__(self, client: AsyncOpenAI) -> None:
		self.client = client
		self.semaphore = Semaphore(self.max_requests_to_image)

	async def ask(
		self,
		user_text: str,
		state: 'FSMContext',
	) -> str:
		return await self._handle_openai_error(self._ask, user_text, state)

	async def _ask(
		self,
		user_text: str,
		state: 'FSMContext',
	) -> str:
		conversation_history = await state.get_data()
		conversation_history = conversation_history.get('history', [])
		conversation_history.append(self._make_content(role='user', user_text=user_text))

		if len(conversation_history) > self.max_history_length:
			conversation_history = conversation_history[-self.max_history_length :]

		async with self.semaphore:
			response = await self.client.chat.completions.create(
				model=self.model,
				messages=conversation_history,
			)

		assistant_reply = response.choices[0].message.content
		conversation_history.append(
			self._make_content(role='assistant', user_text=assistant_reply)
		)

		await state.update_data(history=conversation_history)
		return assistant_reply

	async def generate_image(self, description: str, image_count: int) -> str:
		return await self._handle_openai_error(
			self._generate_image, description, image_count
		)

	async def _generate_image(self, description: str, image_count: int) -> str:
		async with self.semaphore:
			response = await self.client.images.generate(
				prompt=description,
				n=image_count,
				size='1024x1024',
				model='dall-e-2',
				quality='standard',
				response_format='url',
			)
		return response.data[0].url

	@staticmethod
	async def _handle_openai_error(func, *args, **kwargs):
		try:
			return await func(*args, **kwargs)
		except openai.PermissionDeniedError as error:
			raise PermissionOIException(error.message, error.status_code)
		except openai.NotFoundError as error:
			raise NotFoundOIException(error.message, error.status_code)
		except openai.BadRequestError as error:
			raise BadRequestOIException(error.message, error.status_code)
		except openai.RateLimitError as error:
			raise RateLimitImageOIException(error.message, error.status_code)

	@staticmethod
	def _make_content(role: str, user_text: str) -> dict[str, str]:
		return {
			'role': role,
			'content': user_text,
		}
