from enum import StrEnum


class ActionsEnum(StrEnum):
    EXIT = 'Выйти'
    ASK = 'Задать вопрос'
    GENERATE_IMAGE = 'Получить картинку'
    BOT_MANAGEMENT = 'Управление ботом'


class BotEnvEnum(StrEnum):
    DEV = 'dev'
    PROD = 'prod'
    TEST = 'test'


class MessageTypeEnum(StrEnum):
    TEXT = 'text'
    IMAGE_URL = 'image_url'
    VOICE = 'voice'


class BotStatusEnum(StrEnum):
    ON = 'Включить бота'
    MAINTENANCE = 'Перевести на обслуживание'


class RoleEnum(StrEnum):
    USER = 'user'
    ASSISTANT = 'assistant'


class ResponseFormatEnum(StrEnum):
    TEXT = 'text'
    URL = 'url'
