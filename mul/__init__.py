from .ast import *  # noqa
from .interpretation import interpret  # noqa
from .interpretation import Return, SymTable
from .lexer import lex  # noqa
from .parser import parse  # noqa


def exec(prog: str, table: SymTable | None = None) -> Return:
    return interpret(parse(lex(prog)), table or SymTable.root())
