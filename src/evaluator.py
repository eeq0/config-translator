"""Вычисление значений конфигурации по дереву разбора (AST).

Константы вычисляются на этапе трансляции. Объявления let выполняются
по порядку сверху вниз: значение константы вычисляется сразу и
запоминается, а #(ИМЯ) подставляет запомненное значение. Поэтому
константа может использовать только константы, объявленные выше.

Число остаётся числом, словарь struct превращается в словарь Python
с тем же порядком ключей.
"""
from errors import TranslatorError, located
from syntax import ConstRef, Struct


def _lookup(node, constants):
    """Значение константы #(ИМЯ)."""
    name = str(node.name)
    if name not in constants:
        raise TranslatorError(located(
            node.name, f"константа {name} не объявлена"))
    return constants[name]


def _evaluate_struct(node, constants):
    """Вычислить словарь struct { ... }."""
    result = {}
    for pair in node.pairs:
        name = str(pair.name)
        if name in result:
            raise TranslatorError(located(
                pair.name, f"имя {name} повторяется в словаре"))
        result[name] = evaluate_value(pair.value, constants)
    return result


def evaluate_value(node, constants):
    """Вычислить значение: число, словарь или #(ИМЯ)."""
    if isinstance(node, Struct):
        return _evaluate_struct(node, constants)
    if isinstance(node, ConstRef):
        return _lookup(node, constants)
    return node


def evaluate(program):
    """Выполнить объявления let и вернуть итоговое значение."""
    constants = {}
    for declaration in program.lets:
        name = str(declaration.name)
        if name in constants:
            raise TranslatorError(located(
                declaration.name, f"константа {name} уже объявлена"))
        constants[name] = evaluate_value(declaration.value, constants)
    return evaluate_value(program.value, constants)
