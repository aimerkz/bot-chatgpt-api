from typing import TYPE_CHECKING

from utils.enums import MessageTypeEnum
from utils.images import get_image_url
from utils.voice_messages import download_voice_file

if TYPE_CHECKING:
	from aiogram.fsm.context import FSMContext
	from aiogram.types.message import Message

	from clients.openai import OpenAIClient


async def process_text_message(
	message: 'Message',
	openai_client: 'OpenAIClient',
	state: 'FSMContext',
):
	return await openai_client.ask(
		user_text=message.text,
		state=state,
		type_message=MessageTypeEnum.TEXT,
	)


async def process_image_message(
	message: 'Message',
	openai_client: 'OpenAIClient',
	state: 'FSMContext',
):
	image_url = await get_image_url(message)
	return await openai_client.ask(
		image_url=image_url,
		type_message=MessageTypeEnum.IMAGE_URL,
		state=state,
	)


async def process_voice_message(
	message: 'Message',
	openai_client: 'OpenAIClient',
	state: 'FSMContext',
):
	voice_file_path = await download_voice_file(message)
	transcription_text = await openai_client.convert_voice_to_text(voice_file_path)
	answer = await openai_client.ask(
		state=state,
		user_text=transcription_text,
		type_message=MessageTypeEnum.TEXT,
	)
	return answer
