from pydantic import BaseModel


class TextContent(BaseModel):
    role: str
    content: str


class ImageUrl(BaseModel):
    url: str


class ImageContentItem(BaseModel):
    type: str
    image_url: ImageUrl


class ImageContent(BaseModel):
    role: str
    content: list[ImageContentItem]
