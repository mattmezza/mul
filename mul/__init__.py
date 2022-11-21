from dataclasses import dataclass
from typing import Self, Type

from . import lib
from .ast import *  # noqa
from .interpretation import Return, SymTable, interpret
from .lexer import lex
from .parser import parse


def eval(prog: str, table: SymTable | None = None) -> Return:
    return interpret(parse(lex(prog)), table or SymTable.root())


@dataclass(frozen=True)
class Interpreter:
    env: SymTable = SymTable.root()

    def eval(self: Self, prog: str) -> Return:
        return interpret(parse(lex(prog)), self.env)

    @classmethod
    def with_std(cls: Type[Self]) -> Self:
        genv = SymTable.root()
        lib.import_all(genv)
        return cls(genv)
