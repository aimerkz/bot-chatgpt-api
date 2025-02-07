from enum import Enum


class ActionsEnum(str, Enum):
    EXIT = 'Выйти'
    ASK = 'Задать вопрос'
    GENERATE_IMAGE = 'Получить картинку'
