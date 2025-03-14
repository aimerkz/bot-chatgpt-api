import os
from asyncio import Semaphore
from typing import TYPE_CHECKING, assert_never

import openai
from openai import AsyncOpenAI

from exceptions.openai import (
    BadRequestOIException,
    NotFoundOIException,
    PermissionOIException,
    RateLimitOIException,
    ServerOIException,
)
from models.models import ImageContent, ImageContentItem, ImageUrl, TextContent
from utils.enums import MessageTypeEnum
from utils.retry import retry_to_gpt_api

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


class OpenAIClient:
    max_history_length: int = 10
    model: str = 'gpt-4o-mini'
    semaphore: Semaphore
    max_requests_to_api: int = 5

    def __init__(self, client: AsyncOpenAI) -> None:
        self.client = client
        self.semaphore = Semaphore(self.max_requests_to_api)

    @retry_to_gpt_api()
    async def convert_voice_to_text(
        self,
        voice_file_path: str,
    ) -> str | None:
        return await self._handle_openai_error(
            self._convert_voice_to_text,
            voice_file_path,
        )

    async def _convert_voice_to_text(
        self,
        voice_file_path: str,
    ) -> str | None:
        with open(voice_file_path, 'rb') as f:
            async with self.semaphore:
                response = await self.client.audio.transcriptions.create(
                    model='whisper-1',
                    file=f,
                    response_format='text',
                )
        os.remove(voice_file_path)
        return response

    @retry_to_gpt_api()
    async def ask(
        self,
        state: 'FSMContext',
        user_text: str | None = None,
        image_url: str | None = None,
        type_message: MessageTypeEnum = MessageTypeEnum.TEXT,
    ) -> str | None:
        return await self._handle_openai_error(
            self._ask,
            user_text,
            image_url,
            type_message,
            state,
        )

    async def _ask(
        self,
        user_text: str | None,
        image_url: str | None,
        type_message: MessageTypeEnum,
        state: 'FSMContext',
    ) -> str | None:
        conversation_history = await state.get_data()
        conversation_history = conversation_history.get('history', [])

        user_content = self._make_content(
            role='user',
            user_text=user_text,
            image_url=image_url,
            type_message=type_message,
        )

        conversation_history.append(user_content.model_dump())

        if len(conversation_history) > self.max_history_length:
            conversation_history = conversation_history[-self.max_history_length :]

        async with self.semaphore:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=conversation_history,
            )

        assistant_reply = response.choices[0].message.content
        assistant_content = TextContent(role='assistant', content=assistant_reply)
        conversation_history.append(assistant_content.model_dump())

        await state.update_data(history=conversation_history)
        return assistant_reply

    @retry_to_gpt_api()
    async def generate_image(self, description: str) -> str | None:
        return await self._handle_openai_error(self._generate_image, description)

    async def _generate_image(self, description: str) -> str | None:
        async with self.semaphore:
            response = await self.client.images.generate(
                prompt=description,
                n=1,
                size='1024x1024',
                model='dall-e-2',
                quality='standard',
                response_format='url',
            )
        return response.data[0].url

    @staticmethod
    async def _handle_openai_error(func, *args, **kwargs) -> None:
        try:
            return await func(*args, **kwargs)
        except openai.PermissionDeniedError as error:
            raise PermissionOIException(error.message, error.status_code)
        except openai.NotFoundError as error:
            raise NotFoundOIException(error.message, error.status_code)
        except openai.BadRequestError as error:
            raise BadRequestOIException(error.message, error.status_code)
        except openai.RateLimitError as error:
            raise RateLimitOIException(error.message, error.status_code)
        except openai.InternalServerError as error:
            raise ServerOIException(error.message, error.status_code)

    @staticmethod
    def _make_content(
        role: str,
        user_text: str | None = None,
        image_url: str | None = None,
        type_message: MessageTypeEnum = MessageTypeEnum.TEXT,
    ) -> TextContent | ImageContent:
        match type_message:
            case MessageTypeEnum.TEXT:
                return TextContent(role=role, content=user_text)

            case MessageTypeEnum.IMAGE_URL:
                return ImageContent(
                    role=role,
                    content=[
                        ImageContentItem(
                            type=MessageTypeEnum.IMAGE_URL.value,
                            image_url=ImageUrl(url=image_url),
                        )
                    ],
                )

            case _:
                assert assert_never(None)
