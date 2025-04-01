import os
from typing import TYPE_CHECKING

from utils.constants import DOWNLOAD_VOICE_FILES_DIR

if TYPE_CHECKING:
	from aiogram.types.message import Message


async def download_voice_file(message: 'Message') -> str:
	file_info = await message.bot.get_file(message.voice.file_id)
	voice_path = os.path.join(DOWNLOAD_VOICE_FILES_DIR, f'{message.voice.file_id}.ogg')
	await message.bot.download_file(
		file_path=file_info.file_path,
		destination=voice_path,
	)
	return voice_path
