from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Callable, Iterator, Self, Sequence, Tuple
from typing import Type as TType
from typing import Union

from .. import ast
from .symbol_table import SymTable


class Stack:
    def __init__(self: Self):
        self.records = []

    def push(self: Self, val: Any):
        self.records.append(val)

    def pop(self: Self) -> Any:
        return self.records.pop()

    def top(self: Self) -> Any:
        return self.records[-1]


@dataclass(frozen=True)
class Fn:
    params: Tuple[str, ...]
    body: Sequence[ast.AST]
    table: SymTable

    def __str__(self: Self) -> str:
        return "<function>"


@dataclass(frozen=True)
class FnNative:
    py_fn: Callable

    def as_return(self) -> Return:
        return Return.fn_native(self)

    def __str__(self: Self) -> str:
        return "<native>"


@dataclass(frozen=True)
class Return:
    @unique
    class Type(str, Enum):
        NUM = "Num"
        STR = "Str"
        FN = "Fn"
        FN_NATIVE = "FnNative"
        NONE = "None"

    type: Type
    val: Union[float, str, Fn, FnNative] | None

    def __iter__(self) -> Iterator[Union[Type, float, str]]:
        return iter((self.type, self.val))  # type:ignore

    def __str__(self) -> str:
        return "{}: {}".format(*self)

    @classmethod
    def none(cls: TType[Self]) -> Self:
        return cls(Return.Type.NONE, None)

    @classmethod
    def num(cls: TType[Self], n: float) -> Self:
        return cls(Return.Type.NUM, n)

    @classmethod
    def str(cls: TType[Self], s: str) -> Self:
        return cls(Return.Type.STR, s)

    @classmethod
    def fn(cls: TType[Self], fn: Fn) -> Self:
        return cls(Return.Type.FN, fn)

    @classmethod
    def fn_native(cls: TType[Self], fn_native: FnNative) -> Self:
        return cls(Return.Type.FN_NATIVE, fn_native)
