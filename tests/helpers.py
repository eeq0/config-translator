"""Общие помощники для тестов: путь к src и временные файлы."""
import os
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))


def write_temp(test, text, suffix=".conf"):
    """Записать текст во временный файл, удаляемый после теста."""
    handle, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(handle, "w", encoding="utf-8") as file:
        file.write(text)
    test.addCleanup(os.remove, path)
    return path


def value_of(text):
    """Разобрать и вычислить текст конфигурации."""
    from evaluator import evaluate
    from syntax import parse
    return evaluate(parse(text))


def xml_lines(xml_text):
    """Строки XML без заголовка и без отступов."""
    return [line.strip() for line in xml_text.splitlines()[1:]]
