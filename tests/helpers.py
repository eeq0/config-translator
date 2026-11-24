"""Общие помощники для тестов: временные файлы и разбор результата."""
import os
import tempfile

from evaluator import evaluate
from syntax import parse
from tests import ROOT


def write_temp(test, text, suffix=".conf"):
    """Записать текст во временный файл, удаляемый после теста."""
    handle, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(handle, "w", encoding="utf-8") as file:
        file.write(text)
    test.addCleanup(os.remove, path)
    return path


def value_of(text):
    """Разобрать и вычислить текст конфигурации."""
    return evaluate(parse(text))


def examples_path(*parts):
    """Путь к файлу или папке внутри examples."""
    return os.path.join(ROOT, "examples", *parts)


def xml_lines(xml_text):
    """Строки XML без заголовка и без отступов."""
    return [line.strip() for line in xml_text.splitlines()[1:]]
