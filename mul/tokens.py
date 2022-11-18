from dataclasses import dataclass
from typing import Self, Type


@dataclass(frozen=True)
class Token:
    def is_a(self: Self, type: Type[Self]) -> bool:
        return isinstance(self, type)


@dataclass(frozen=True, repr=True)
class Val(Token):
    val: str


@dataclass(frozen=True)
class Num(Val):
    ...


@dataclass(frozen=True)
class Str(Val):
    ...


@dataclass(frozen=True)
class Sym(Val):
    ...


@dataclass(frozen=True)
class Comma(Token):
    ...


@dataclass(frozen=True)
class Colon(Token):
    ...


@dataclass(frozen=True)
class Semi(Token):
    ...


@dataclass(frozen=True)
class LPar(Token):
    ...


@dataclass(frozen=True)
class RPar(Token):
    ...


@dataclass(frozen=True)
class LBrace(Token):
    ...


@dataclass(frozen=True)
class RBrace(Token):
    ...


@dataclass(frozen=True)
class Plus(Token):
    ...


@dataclass(frozen=True)
class Min(Token):
    ...


@dataclass(frozen=True)
class Mul(Token):
    ...


@dataclass(frozen=True)
class Div(Token):
    ...


@dataclass(frozen=True)
class Eq(Token):
    ...
