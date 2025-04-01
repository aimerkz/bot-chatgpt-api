from typing import Literal

from pydantic import BaseModel


class TextContent(BaseModel):
    role: str
    content: str


class ImageUrl(BaseModel):
    url: str


class ImageContentItem(BaseModel):
    type: Literal['image_url']
    image_url: ImageUrl


class ImageContent(BaseModel):
    role: str
    content: list[ImageContentItem]
