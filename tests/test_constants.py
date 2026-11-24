"""Тесты констант: let ИМЯ = значение; и #(ИМЯ)."""
import unittest

import helpers
from errors import TranslatorError


class ConstantTest(unittest.TestCase):
    """Объявление и вычисление констант на этапе трансляции."""

    def test_number_constant(self):
        """Константа-число подставляется в словарь."""
        text = "let PORT = 8080;\nstruct { PORT = #(PORT) }"
        self.assertEqual(helpers.value_of(text), {"PORT": 8080})

    def test_struct_constant(self):
        """Константа-словарь подставляется целиком."""
        text = ("let LIMITS = struct { MIN = -5, MAX = 5 };\n"
                "struct { A = #(LIMITS), B = #(LIMITS) }")
        limits = {"MIN": -5, "MAX": 5}
        self.assertEqual(helpers.value_of(text),
                         {"A": limits, "B": limits})

    def test_constant_uses_constant(self):
        """Константа может использовать константы, объявленные выше."""
        text = ("let X = 1;\nlet Y = struct { X = #(X) };\n"
                "let Z = struct { Y = #(Y), W = struct { X = #(X) } };\n"
                "#(Z)")
        self.assertEqual(helpers.value_of(text),
                         {"Y": {"X": 1}, "W": {"X": 1}})

    def test_top_level_reference(self):
        """Итоговым значением может быть сама константа."""
        self.assertEqual(helpers.value_of("let A = -3; #(A)"), -3)

    def test_deep_nesting(self):
        """#(ИМЯ) внутри вложенных словарей."""
        text = ("let N = 7;\n"
                "struct { A = struct { B = struct { C = #(N) } } }")
        self.assertEqual(helpers.value_of(text),
                         {"A": {"B": {"C": 7}}})

    def test_constant_and_key_same_name(self):
        """Имя константы и имя ключа не мешают друг другу."""
        text = "let A = 1; struct { A = #(A), B = struct { A = 2 } }"
        self.assertEqual(helpers.value_of(text),
                         {"A": 1, "B": {"A": 2}})


class ConstantErrorTest(unittest.TestCase):
    """Ошибки при работе с константами."""

    def check(self, text, *parts):
        """Убедиться, что текст даёт ошибку со всеми частями сообщения."""
        with self.assertRaises(TranslatorError) as context:
            helpers.value_of(text)
        for part in parts:
            self.assertIn(part, str(context.exception))

    def test_not_declared(self):
        """Константа не объявлена."""
        self.check("struct {\n  A = #(B)\n}", "строка 2, столбец 9",
                   "константа B не объявлена")

    def test_declared_below(self):
        """Константу нельзя использовать до объявления."""
        self.check("let A = #(B);\nlet B = 1;\n#(A)",
                   "константа B не объявлена")

    def test_declared_twice(self):
        """Повторное объявление константы."""
        self.check("let A = 1;\nlet A = 2;\n#(A)", "строка 2",
                   "константа A уже объявлена")

    def test_missing_semicolon(self):
        """После объявления нужна точка с запятой."""
        self.check("let A = 1\n#(A)", "неожиданный элемент «#(»", "«;»")

    def test_only_declarations(self):
        """После объявлений нужно итоговое значение."""
        self.check("let A = 1;", "неожиданный конец файла", "«let»")

    def test_lowercase_constant(self):
        """Имя константы — только большие латинские буквы."""
        self.check("let a = 1; #(a)", "недопустимый символ «a»",
                   "ожидалось: имя (большие латинские буквы)")

    def test_unclosed_reference(self):
        """Не закрыта скобка в #(ИМЯ)."""
        self.check("let A = 1; #(A", "неожиданный конец файла", "«)»")


if __name__ == "__main__":
    unittest.main()
