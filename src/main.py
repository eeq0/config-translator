"""Точка входа: python3 src/main.py --input ФАЙЛ.

Читает текст на учебном конфигурационном языке из файла, путь к которому
задан ключом --input, и выводит результат на языке XML в стандартный
вывод. Ошибки выводятся в стандартный поток ошибок, код возврата 1.
"""
import argparse
import sys

from errors import TranslatorError
from evaluator import evaluate
from syntax import parse
from xml_writer import to_xml

EXIT_ERROR = 1


def read_source(path):
    """Прочитать текст конфигурации из файла."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError as err:
        raise TranslatorError(f"файл не найден: {path}") from err
    except (OSError, UnicodeError) as err:
        raise TranslatorError(f"не удалось прочитать файл: {path}") from err


def translate(text):
    """Перевести текст конфигурации в текст XML."""
    return to_xml(evaluate(parse(text)))


def parse_args(argv):
    """Разобрать аргументы командной строки."""
    parser = argparse.ArgumentParser(
        prog="run.sh",
        description="Транслятор учебного конфигурационного языка в XML")
    parser.add_argument("-i", "--input", required=True,
                        help="путь к файлу с конфигурацией")
    return parser.parse_args(argv)


def main(argv=None):
    """Выполнить трансляцию и вернуть код завершения."""
    args = parse_args(argv)
    try:
        result = translate(read_source(args.input))
    except TranslatorError as err:
        print(f"ошибка: {err}", file=sys.stderr)
        return EXIT_ERROR
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
