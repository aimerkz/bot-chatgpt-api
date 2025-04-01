from enum import Enum


class ActionsEnum(str, Enum):
    EXIT = 'Выйти'
    ASK = 'Задать вопрос'
    GENERATE_IMAGE = 'Получить картинку'
    BOT_MANAGEMENT = 'Управление ботом'


class BotEnvEnum(str, Enum):
    DEV = 'dev'
    PROD = 'prod'


class MessageTypeEnum(str, Enum):
    TEXT = 'text'
    IMAGE_URL = 'image_url'
    VOICE = 'voice'


class BotStatusEnum(str, Enum):
    ON = 'Включить бота'
    MAINTENANCE = 'Перевести на обслуживание'
