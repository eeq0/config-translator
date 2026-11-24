"""Тесты запуска из командной строки."""
import contextlib
import io
import unittest

from tests import helpers
from main import main


def run_main(argv):
    """Запустить main и вернуть (код, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class MainTest(unittest.TestCase):
    """Ключ --input, вывод XML и ошибок."""

    def test_translate_file(self):
        """Файл переводится в XML на стандартный вывод."""
        path = helpers.write_temp(self, "struct { A = 1 }\n")
        code, out, err = run_main(["--input", path])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("<A>1</A>", out)

    def test_short_key(self):
        """Короткая форма ключа -i."""
        path = helpers.write_temp(self, "7")
        code, out, _ = run_main(["-i", path])
        self.assertEqual(code, 0)
        self.assertIn("<config>7</config>", out)

    def test_constants(self):
        """Константы вычисляются, в XML попадают значения."""
        path = helpers.write_temp(
            self, "let N = 3;\nstruct { A = #(N), B = struct { C = #(N) } }")
        code, out, _ = run_main(["--input", path])
        self.assertEqual(code, 0)
        self.assertEqual(helpers.xml_lines(out), [
            "<config>", "<A>3</A>", "<B>", "<C>3</C>", "</B>", "</config>"])

    def test_syntax_error(self):
        """Синтаксическая ошибка: код 1, сообщение в stderr."""
        path = helpers.write_temp(self, "struct { A = }")
        code, out, err = run_main(["--input", path])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("ошибка: строка 1", err)

    def test_missing_file(self):
        """Файла нет."""
        code, _, err = run_main(["--input", "no_such_file.conf"])
        self.assertEqual(code, 1)
        self.assertIn("файл не найден", err)

    def test_key_is_required(self):
        """Без ключа --input argparse завершает программу."""
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                main([])


if __name__ == "__main__":
    unittest.main()
