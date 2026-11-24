"""Перевод вычисленной конфигурации в текст на языке XML.

Корневой элемент называется config. Каждый ключ словаря становится
элементом с тем же именем, число становится текстом элемента:

    struct { PORT = 80 }   ->   <config><PORT>80</PORT></config>
"""
from xml.etree import ElementTree

ROOT_TAG = "config"
HEADER = '<?xml version="1.0" encoding="UTF-8"?>'


def _fill(element, value):
    """Записать значение внутрь элемента XML."""
    if isinstance(value, dict):
        for name, item in value.items():
            _fill(ElementTree.SubElement(element, name), item)
    else:
        element.text = str(value)


def to_xml(value):
    """Вернуть текст XML для вычисленного значения."""
    root = ElementTree.Element(ROOT_TAG)
    _fill(root, value)
    ElementTree.indent(root)
    return HEADER + "\n" + ElementTree.tostring(root, encoding="unicode")
