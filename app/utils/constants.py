from pathlib import Path

from aiogram import html

DOWNLOAD_VOICE_FILES_DIR = Path(__file__).resolve().parent.parent.parent / 'voices'
DOWNLOAD_VOICE_FILES_DIR.mkdir(parents=True, exist_ok=True)

help_text = (
    f'{html.italic(html.bold("Доступные действия:"))}\n\n'
    f'{html.bold("1. Задать вопрос")} — чтобы задать новый вопрос боту (текст, загрузка фото или голосовое сообщение)\n\n'
    f'{html.bold("2. Выйти")} — чтобы выйти из текущего диалога\n\n'
    f'{html.bold("3. Получить картинку")} — сгенерировать картинку (от 1 до 3) по запросу\n\n'
    f'{html.bold("Активируй бота командной /start, чтобы продолжить!")}\n\n'
    f'{html.spoiler(html.link("Код бота на GitHub", "https://github.com/aimerkz/bot-chatgpt-api"))}'
)
