"""Синтаксический разбор учебного конфигурационного языка.

Используется специализированный инструмент разбора Lark: грамматика
записана в файле grammar.lark, по ней Lark строит LALR-парсер.
Дерево разбора Lark превращается в простое дерево (AST):

    число                       -> int
    struct { ИМЯ = значение }   -> Struct (список пар Pair)
    #(ИМЯ)                      -> ConstRef
    let ИМЯ = значение;         -> Let
    весь текст                  -> Program (объявления Let и значение)
"""
from collections import namedtuple

from lark import Lark, Transformer, UnexpectedCharacters, UnexpectedInput

from errors import TranslatorError

PARSER = Lark.open("grammar.lark", rel_to=__file__, parser="lalr")
END = "$END"
READABLE = {
    "NAME": "имя (большие латинские буквы)",
    "NUMBER": "число",
    END: "конец файла",
}

Pair = namedtuple("Pair", "name value")
Struct = namedtuple("Struct", "pairs")
ConstRef = namedtuple("ConstRef", "name")
Let = namedtuple("Let", "name value")
Program = namedtuple("Program", "lets value")


class ToAst(Transformer):
    """Превращает дерево разбора Lark в простое дерево (AST)."""

    def number(self, items):
        """Число: [+-]?\\d+."""
        return int(items[0])

    def pair(self, items):
        """Пара «ИМЯ = значение» внутри словаря."""
        return Pair(items[0], items[1])

    def struct(self, items):
        """Словарь struct { ... }."""
        return Struct(list(items))

    def const_ref(self, items):
        """Вычисление константы #(ИМЯ)."""
        return ConstRef(items[0])

    def let_decl(self, items):
        """Объявление константы let ИМЯ = значение;."""
        return Let(items[0], items[1])

    def start(self, items):
        """Весь текст: объявления констант, затем значение."""
        return Program(list(items[:-1]), items[-1])


def _describe(name):
    """Понятное название элемента, который ожидал парсер."""
    if name in READABLE:
        return READABLE[name]
    return f"«{PARSER.get_terminal(name).pattern.value}»"


def _expected(err):
    """Что парсер мог принять в месте ошибки."""
    if getattr(err, "interactive_parser", None) is not None:
        return err.interactive_parser.accepts()
    return err.expected


def _syntax_message(err):
    """Текст синтаксической ошибки: где, что встретилось, что ожидалось."""
    if isinstance(err, UnexpectedCharacters):
        found = f"недопустимый символ «{err.char}»"
    elif err.token.type == END:
        found = "неожиданный конец файла"
    else:
        found = f"неожиданный элемент «{err.token}»"
    names = ", ".join(sorted(_describe(name) for name in _expected(err)))
    return (f"строка {err.line}, столбец {err.column}: {found}; "
            f"ожидалось: {names}")


def parse(text):
    """Разобрать текст конфигурации и вернуть AST (Program)."""
    try:
        tree = PARSER.parse(text)
    except UnexpectedInput as err:
        raise TranslatorError(_syntax_message(err)) from err
    return ToAst().transform(tree)
