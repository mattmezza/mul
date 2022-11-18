import sys
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Mapping, Self, Type, cast


@dataclass(frozen=True)
class IO:
    stdin: BytesIO
    stdout: BytesIO
    stderr: BytesIO


@dataclass(frozen=True)
class SymTable:
    symbols: Mapping[str, Any]
    parent: Self | None = None
    io: IO | None = None

    def lookup(self: Self, name: str) -> Any | None:
        val = self.symbols.get(name)
        if val is None:
            if self.has_parent():
                return cast(Self, self.parent).lookup(name)
            return None
        return val

    def has_parent(self: Self) -> bool:
        return self.parent is not None

    def has_io(self: Self) -> bool:
        return self.io is not None

    def put(self: Self, name: str, val: Any) -> Self:
        self.symbols.update({name: val})
        return self

    def __contains__(self: Self, name: str) -> bool:
        return name in self.symbols

    def child(self: Self) -> Self:
        return self.with_parent(self)

    def stdin(self: Self) -> BytesIO | None:
        if self.has_io():
            return self.io.stdin
        else:
            return self.parent.stdin() if self.has_parent() else None

    def stdout(self: Self) -> BytesIO | None:
        if self.has_io():
            return self.io.stdout
        else:
            return self.parent.stdout() if self.has_parent() else None

    def stderr(self: Self) -> BytesIO | None:
        if self.has_io():
            return self.io.stderr
        else:
            return self.parent.stderr() if self.has_parent() else None

    @classmethod
    def with_parent(cls: Type[Self], parent: Self) -> Self:
        return cls({}, parent)

    @classmethod
    def root(cls: Type[Self]) -> Self:
        return cls({}, None, IO(sys.stdin, sys.stdout, sys.stderr))
