from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class Lookahead(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self.iterator = iter(iterable)
        self.look()

    def look(self) -> None:
        try:
            self.ahead = next(self.iterator)
        except StopIteration:
            self.ahead = None

    def next(self) -> T | None:
        prev = self.ahead
        self.look()
        return prev

    def peek(self) -> T | None:
        return self.ahead
