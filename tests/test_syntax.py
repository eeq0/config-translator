"""Тесты синтаксического разбора: числа, словари, ошибки."""
import unittest

import helpers
from errors import TranslatorError


class NumberTest(unittest.TestCase):
    """Числа: [+-]?\\d+."""

    def test_numbers(self):
        """Без знака, с плюсом, с минусом, ноль."""
        cases = {"42": 42, "+7": 7, "-15": -15, "0": 0, "007": 7}
        for text, expected in cases.items():
            self.assertEqual(helpers.value_of(text), expected, msg=text)

    def test_spaces_and_lines(self):
        """Пробелы и переводы строк вокруг значения игнорируются."""
        self.assertEqual(helpers.value_of("\n   12  \n"), 12)


class StructTest(unittest.TestCase):
    """Словари struct { ИМЯ = значение, ... }."""

    def test_empty(self):
        """Пустой словарь."""
        self.assertEqual(helpers.value_of("struct {}"), {})

    def test_pairs_and_order(self):
        """Несколько пар, порядок ключей сохраняется."""
        result = helpers.value_of("struct { B = 2, A = -1, C = +3 }")
        self.assertEqual(list(result.items()),
                         [("B", 2), ("A", -1), ("C", 3)])

    def test_trailing_comma(self):
        """Запятая после последней пары разрешена."""
        self.assertEqual(helpers.value_of("struct {\n  A = 1,\n  B = 2,\n}"),
                         {"A": 1, "B": 2})

    def test_nested(self):
        """Словари внутри словарей на нескольких уровнях."""
        text = ("struct { A = struct { B = struct { C = 1, D = struct {} },"
                " E = 2 }, F = 3 }")
        self.assertEqual(helpers.value_of(text),
                         {"A": {"B": {"C": 1, "D": {}}, "E": 2}, "F": 3})

    def test_duplicate_name(self):
        """Повтор имени в одном словаре — ошибка с номером строки."""
        with self.assertRaisesRegex(TranslatorError,
                                    "строка 2.*A повторяется"):
            helpers.value_of("struct {\n A = 1, A = 2 }")


class SyntaxErrorTest(unittest.TestCase):
    """Синтаксические ошибки с понятными сообщениями."""

    def check(self, text, *parts):
        """Убедиться, что текст даёт ошибку со всеми частями сообщения."""
        with self.assertRaises(TranslatorError) as context:
            helpers.value_of(text)
        for part in parts:
            self.assertIn(part, str(context.exception))

    def test_lowercase_name(self):
        """Имя только из больших латинских букв."""
        self.check("struct { port = 1 }", "строка 1, столбец 10",
                   "недопустимый символ «p»")

    def test_missing_comma(self):
        """Между парами нужна запятая."""
        self.check("struct { A = 1 B = 2 }", "неожиданный элемент «B»",
                   "«,»", "«}»")

    def test_unclosed_struct(self):
        """Словарь не закрыт."""
        self.check("struct { A = 1", "неожиданный конец файла")

    def test_not_integer(self):
        """Дробных чисел нет."""
        self.check("struct { A = 1.5 }", "недопустимый символ «.»",
                   "ожидалось: «,», «}»")

    def test_empty_text(self):
        """Пустой файл: нужно значение."""
        self.check("", "неожиданный конец файла", "число")

    def test_extra_value(self):
        """После значения ничего быть не должно."""
        self.check("struct { A = 1 } 5", "неожиданный элемент «5»",
                   "конец файла")

    def test_missing_value(self):
        """После знака = нужно значение."""
        self.check("struct { A = }", "неожиданный элемент «}»", "число")


if __name__ == "__main__":
    unittest.main()
