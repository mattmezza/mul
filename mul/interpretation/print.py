from __future__ import annotations

from typing import Tuple, Union

from .. import ast
from .activation_record import Fn, Return
from .symbol_table import SymTable
from .visitor import Visitor


class PrettyPrint(Visitor):
    def __init__(self, step: int):
        self.level = 0
        self.step = step
        self.table = SymTable.root()

    def incr(self) -> int:
        self.level += self.step
        return self.level

    def decr(self) -> int:
        self.level -= self.step
        return self.level

    def print(self, s: str) -> None:
        print(" " * self.level, s)

    def num(self, tree: ast.Num) -> Return:
        self.print(str(tree.val))
        return Return.none()

    def str(self, tree: ast.Str) -> Return:
        self.print(f'"{tree.val}"')
        return Return.none()

    def op_diadic(self, tree: ast.OpDiadic) -> Return:
        self.print(str(tree.operator))
        self.incr()
        self.visit(tree.left)
        self.visit(tree.right)
        self.decr()
        return Return.none()

    def sym(self, tree: ast.Sym) -> Return:
        self.print(f"${tree.val}")
        return Return.none()

    def seq(self, tree: ast.Seq) -> Tuple[Union[Return, Fn, Tuple[str]]]:
        self.print("...")
        self.incr()
        for subtree in tree:
            self.visit(subtree)
        return (Return.none(),)

    def fn(self, tree: ast.Fn) -> Fn:
        self.print("def")
        self.incr()
        self.params(tree.params)
        self.seq(tree.body)
        self.decr()
        return Fn(tuple(), tree.body, self.table)

    def call(self, tree: ast.Call) -> Return:
        self.print("call")
        self.incr()
        self.sym(tree.sym)
        self.incr()
        self.seq(tree.args)
        self.decr()
        self.decr()
        return Return.none()

    def params(self, tree: ast.Params) -> Tuple[str]:
        self.print("params")
        self.incr()
        for s in tree.symbols:
            self.sym(s)
        self.decr()
        return tuple()

    def assignment(self, tree: ast.Assignment) -> Return:
        self.print("=")
        self.incr()
        self.sym(tree.sym)
        self.visit(tree.val)
        self.decr()
        return Return.none()


def pprint(tree: ast.AST) -> None:
    for subtree in tree:
        visitor = PrettyPrint(2)
        visitor.visit(subtree)
