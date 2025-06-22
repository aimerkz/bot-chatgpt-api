import re

_ESCAPE_CHARS = r'_*[]()~`>#+-=|{}.!'


class TelegramMarkdownV2Formatter:
    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        return re.sub(f'([{re.escape(_ESCAPE_CHARS)}])', r'\\\1', text)

    @staticmethod
    def has_code_blocks(text: str) -> bool:
        return re.search(r'```[a-zA-Z]*\n[\s\S]+?```', text) is not None

    @staticmethod
    def strip_code_lang_markers(text: str) -> str:
        if TelegramMarkdownV2Formatter.has_code_blocks(text):
            return re.sub(r'```[a-zA-Z]+\n', '```', text)
        return text

    @staticmethod
    def format_answer_simple(answer: str) -> str:
        answer = TelegramMarkdownV2Formatter.strip_code_lang_markers(answer)
        escaped_text = TelegramMarkdownV2Formatter.escape_markdown_v2(answer)

        # Жирный текст
        escaped_text = re.sub(r'\\\*\\\*(.+?)\\\*\\\*', r'*\1*', escaped_text)

        # Курсив
        escaped_text = re.sub(r'\\\*(.+?)\\\*', r'_\1_', escaped_text)

        # Inline код
        escaped_text = re.sub(r'\\`([^\\`\n]+)\\`', r'`\1`', escaped_text)

        # Блок кода
        escaped_text = re.sub(
            r'\\`\\`\\`([\s\S]+?)\\`\\`\\`', r'```\n\1\n```', escaped_text
        )

        return escaped_text
