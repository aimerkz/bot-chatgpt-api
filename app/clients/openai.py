import os
from asyncio import Semaphore
from typing import TYPE_CHECKING, assert_never

import openai
from openai import AsyncOpenAI

from exceptions import openai as openai_exceptions
from models.models import ImageContent, ImageContentItem, ImageUrl, TextContent
from utils import constants, enums

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


class OpenAIClient:
    max_history_length: int = constants.MAX_HISTORY_LENGTH
    model: str = constants.GPT_MODEL
    semaphore: Semaphore
    max_requests_to_api: int = constants.MAX_REQUESTS_TO_GPT_API

    def __init__(self, client: AsyncOpenAI) -> None:
        self.client = client
        self.semaphore = Semaphore(self.max_requests_to_api)

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
        with open(voice_file_path, mode='rb') as voice_file:
            async with self.semaphore:
                response = await self.client.audio.transcriptions.create(  # type: ignore
                    model=constants.GPT_AUDIO_MODEL,
                    file=voice_file,
                    response_format=enums.ResponseFormatEnum.TEXT,
                    timeout=constants.TIMEOUT,
                )
        os.remove(voice_file_path)
        return response

    async def ask(
        self,
        state: 'FSMContext',
        user_text: str | None = None,
        image_url: str | None = None,
        type_message: enums.MessageTypeEnum = enums.MessageTypeEnum.TEXT,
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
        type_message: enums.MessageTypeEnum,
        state: 'FSMContext',
    ) -> str | None:
        conversation_history = await state.get_data()
        conversation_history = conversation_history.get('history', [])

        user_content = self._make_content(
            role=enums.RoleEnum.USER,
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
                timeout=constants.TIMEOUT,
            )

        assistant_reply = response.choices[0].message.content
        assistant_content = TextContent(
            role=enums.RoleEnum.ASSISTANT, content=assistant_reply
        )
        conversation_history.append(assistant_content.model_dump())

        await state.update_data(history=conversation_history)
        return assistant_reply

    async def generate_image(self, description: str) -> str | None:
        return await self._handle_openai_error(self._generate_image, description)

    async def _generate_image(self, description: str) -> str | None:
        async with self.semaphore:
            response = await self.client.images.generate(
                prompt=description,
                n=1,
                size=constants.IMAGE_SIZE,  # type: ignore
                model=constants.GPT_IMAGE_MODEL,
                response_format=enums.ResponseFormatEnum.URL,  # type: ignore
                timeout=constants.TIMEOUT,
            )
        return response.data[0].url

    @staticmethod
    async def _handle_openai_error(func, *args, **kwargs) -> None:
        try:
            return await func(*args, **kwargs)
        except openai.PermissionDeniedError as error:
            raise openai_exceptions.PermissionOIException(
                error.message, error.status_code
            )
        except openai.NotFoundError as error:
            raise openai_exceptions.NotFoundOIException(error.message, error.status_code)
        except openai.BadRequestError as error:
            raise openai_exceptions.BadRequestOIException(
                error.message, error.status_code
            )
        except openai.RateLimitError as error:
            raise openai_exceptions.RateLimitOIException(error.message, error.status_code)
        except openai.InternalServerError as error:
            raise openai_exceptions.ServerOIException(error.message, error.status_code)
        except openai.AuthenticationError as error:
            raise openai_exceptions.AuthenticationOIException(
                error.message, error.status_code
            )
        except openai.APITimeoutError as error:
            raise openai_exceptions.TimedOutOIException(error.message)

    @staticmethod
    def _make_content(
        role: str,
        user_text: str | None = None,
        image_url: str | None = None,
        type_message: enums.MessageTypeEnum = enums.MessageTypeEnum.TEXT,
    ) -> TextContent | ImageContent:
        match type_message:
            case enums.MessageTypeEnum.TEXT:
                return TextContent(role=role, content=user_text)

            case enums.MessageTypeEnum.IMAGE_URL:
                return ImageContent(
                    role=role,
                    content=[
                        ImageContentItem(
                            type=enums.MessageTypeEnum.IMAGE_URL,
                            image_url=ImageUrl(url=image_url),
                        )
                    ],
                )

            case _:
                assert_never(None)
