from .ast import *  # noqa
from .interpretation import interpret  # noqa
from .interpretation import Return, SymTable
from .lexer import lex  # noqa
from .parser import parse  # noqa
from . import lib


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
