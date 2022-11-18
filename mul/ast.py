from dataclasses import dataclass, replace
from enum import Enum, auto, unique
from typing import Iterable, Self, Tuple, Type, Union


@dataclass(frozen=True)
class AST:
    def is_a(self: Self, type: Type[Self]) -> bool:
        return isinstance(self, type)


@dataclass(frozen=True)
class Seq(AST):
    children: Tuple[AST, ...]
    replace = replace

    def __iter__(self: Self) -> Iterable[AST]:
        return iter(self.children)


@dataclass(frozen=True)
class Val(AST):
    val: Union[float, str]


@dataclass(frozen=True)
class Num(Val):
    val: float


@dataclass(frozen=True)
class Str(Val):
    val: str


@dataclass(frozen=True)
class Sym(Val):
    val: str


@dataclass(frozen=True)
class OpDiadic(AST):
    @unique
    class Operator(Enum):
        SUM = auto()
        MIN = auto()
        MUL = auto()
        DIV = auto()

    operator: Operator
    left: AST
    right: AST

    @classmethod
    def sum(cls: Type[Self], left: AST, right: AST) -> Self:
        return cls(OpDiadic.Operator.SUM, left, right)

    @classmethod
    def min(cls: Type[Self], left: AST, right: AST) -> Self:
        return cls(OpDiadic.Operator.MIN, left, right)

    @classmethod
    def mul(cls: Type[Self], left: AST, right: AST) -> Self:
        return cls(OpDiadic.Operator.MUL, left, right)

    @classmethod
    def div(cls: Type[Self], left: AST, right: AST) -> Self:
        return cls(OpDiadic.Operator.DIV, left, right)


@dataclass(frozen=True)
class Params(AST):
    symbols: Tuple[Sym, ...]


@dataclass(frozen=True)
class Fn(AST):
    params: Params
    body: Seq


@dataclass(frozen=True)
class Call(AST):
    sym: Sym
    args: Seq


@dataclass(frozen=True)
class Assignment(AST):
    sym: Sym
    val: AST
