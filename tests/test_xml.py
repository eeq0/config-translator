"""Тесты перевода значений в XML."""
import unittest
from xml.etree import ElementTree

from tests import helpers
from xml_writer import HEADER, to_xml


class XmlTest(unittest.TestCase):
    """Вид выходного XML."""

    def test_number(self):
        """Число становится текстом корневого элемента."""
        self.assertEqual(to_xml(5), HEADER + "\n<config>5</config>")

    def test_empty_struct(self):
        """Пустой словарь — пустой корневой элемент."""
        self.assertEqual(to_xml({}), HEADER + "\n<config />")

    def test_nested_struct(self):
        """Ключи становятся элементами, вложенность сохраняется."""
        text = to_xml({"SERVER": {"PORT": 80, "LIMITS": {}}, "DEBUG": 0})
        self.assertEqual(helpers.xml_lines(text), [
            "<config>",
            "<SERVER>",
            "<PORT>80</PORT>",
            "<LIMITS />",
            "</SERVER>",
            "<DEBUG>0</DEBUG>",
            "</config>",
        ])

    def test_well_formed(self):
        """Результат читается стандартным разборщиком XML."""
        root = ElementTree.fromstring(to_xml({"A": {"B": -3}}))
        self.assertEqual(root.find("A/B").text, "-3")


if __name__ == "__main__":
    unittest.main()
