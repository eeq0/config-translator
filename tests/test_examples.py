"""Тесты примеров из папки examples."""
import glob
import os
import unittest
from xml.etree import ElementTree

import helpers
from errors import TranslatorError
from main import read_source, translate

EXAMPLES = os.path.join(helpers.ROOT, "examples")


def translate_example(name):
    """Перевести пример в XML и вернуть корневой элемент."""
    text = read_source(os.path.join(EXAMPLES, name))
    return ElementTree.fromstring(translate(text))


class ExamplesTest(unittest.TestCase):
    """Два примера из разных предметных областей и примеры ошибок."""

    def test_web_server(self):
        """Веб-сервер: константы подставлены в несколько мест."""
        root = translate_example("web_server.conf")
        self.assertEqual(root.find("SERVER/PORT").text, "8080")
        self.assertEqual(root.find("PROXY/TARGET").text, "8080")
        self.assertEqual(root.find("SERVER/LIMITS/CONNECTIONS").text, "1000")

    def test_smart_home(self):
        """Умный дом: отрицательные числа, константа-словарь."""
        root = translate_example("smart_home.conf")
        self.assertEqual(root.find("HOUSE/OUTSIDE/MIN").text, "-25")
        self.assertEqual(root.find("ROOMS/KITCHEN/LIGHT/COLOR").text, "3000")
        self.assertEqual(list(root.find("ROOMS/GARAGE/LIGHT")), [])

    def test_error_examples(self):
        """Каждый пример из examples/errors даёт ошибку."""
        paths = sorted(glob.glob(os.path.join(EXAMPLES, "errors", "*.conf")))
        self.assertTrue(paths)
        for path in paths:
            with self.assertRaises(TranslatorError, msg=path):
                translate(read_source(path))


if __name__ == "__main__":
    unittest.main()
