"""Вычисление значений конфигурации по дереву разбора (AST).

Число остаётся числом, словарь struct превращается в словарь Python
с тем же порядком ключей. Повтор имени внутри словаря является ошибкой.
"""
from errors import TranslatorError, located
from syntax import Struct


def _evaluate_struct(node):
    """Вычислить словарь struct { ... }."""
    result = {}
    for pair in node.pairs:
        name = str(pair.name)
        if name in result:
            raise TranslatorError(located(
                pair.name, f"имя {name} повторяется в словаре"))
        result[name] = evaluate_value(pair.value)
    return result


def evaluate_value(node):
    """Вычислить значение: число или словарь."""
    if isinstance(node, Struct):
        return _evaluate_struct(node)
    return node


def evaluate(program):
    """Вычислить всю конфигурацию и вернуть итоговое значение."""
    return evaluate_value(program.value)
