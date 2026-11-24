"""Исключения транслятора."""


class TranslatorError(Exception):
    """Ошибка трансляции: её текст показывается пользователю."""


def located(token, message):
    """Добавить к сообщению строку и столбец, где стоит элемент."""
    return f"строка {token.line}, столбец {token.column}: {message}"
