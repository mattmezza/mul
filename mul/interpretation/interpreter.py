from __future__ import annotations

from inspect import signature
from operator import attrgetter
from typing import Any, Iterable, Self, Sequence, Tuple, Union

from .. import ast
from .activation_record import Fn, Return, Stack
from .symbol_table import SymTable
from .visitor import Visitor


class Interpreter(Visitor):
    def __init__(self: Self, glob: SymTable):
        self.tables = Stack()
        self.tables.push(glob)

    def params(self: Self, tree: ast.Params) -> Sequence[str]:
        return tuple(map(attrgetter("val"), tree.symbols))

    def num(self: Self, tree: ast.Num) -> Return:
        return Return.num(float(tree.val))

    def str(self: Self, tree: ast.Str) -> Return:
        return Return.str(tree.val)

    def op_diadic(self: Self, tree: ast.OpDiadic) -> Return:
        left_type, left = self.visit(tree.left)
        right_type, right = self.visit(tree.right)
        op = tree.operator
        if op == ast.OpDiadic.Operator.SUM:
            res = left + right
        elif op == ast.OpDiadic.Operator.MIN:
            res = left - right
        elif op == ast.OpDiadic.Operator.MUL:
            res = left * right
        elif op == ast.OpDiadic.Operator.DIV:
            res = left / right
        else:
            raise Exception(f"Invalid operation: '{op}'.")
        return Return.num(res)

    def sym(self: Self, tree: ast.Sym) -> Return:
        sym = self.tables.top().lookup(tree.val)
        if sym is None:
            raise Exception(f"Unknown symbol '{tree.val}'.")
        return sym

    def fn(self: Self, tree: ast.Fn) -> Fn:
        params = self.params(tree.params)
        body = tree.body
        return Return.fn(Fn(params, body, self.tables.top().child()))

    def seq(
        self: Self, tree: ast.Seq
    ) -> Sequence[Union[Return, Fn, Tuple[str]]]:
        return tuple(map(self.visit, tree.children))

    def call(self: Self, tree: ast.Call) -> Return:
        ret = self.sym(tree.sym)
        fn = ret.val
        args = self.seq(tree.args)
        if ret.type == Return.Type.FN:
            if len(fn.params) != len(args):
                raise Exception(
                    f"Fn {tree.sym.val} requires {len(fn.params)} parameters "
                    f"but {len(args)} were passed."
                )
            override_table = fn.table.child()
            for param, arg in zip(fn.params, args):
                override_table.put(param, arg)
            self.tables.push(override_table)

            res = self.seq(fn.body)
            self.tables.pop()
            return res[-1]
        elif ret.type == Return.Type.FN_NATIVE:
            params = signature(fn.py_fn).parameters
            if (len(params) - 1) != len(args):
                raise Exception(
                    f"Fn {tree.sym.val} requires {len(params) - 1} parameters "
                    f"but {len(args)} were passed."
                )
            return fn.py_fn(self.tables.top(), *args)
        else:
            raise Exception(f"{fn} is not a fn.")

    def assignment(self: Self, tree: ast.Assignment) -> Return:
        name = tree.sym.val
        if name in self.tables.top():
            raise Exception(f"Cannot re-assign symbol '{name}'.")
        val = self.visit(tree.val)
        self.tables.top().put(name, val)
        return val


def expressions(
    interpreter: Interpreter, tree: Iterable[ast.Seq]
) -> Iterable[Any]:
    for subtree in tree:
        yield interpreter.visit(subtree)


def interpret(tree: Iterable[ast.Seq], table: SymTable) -> Any:
    result = None
    for expr in expressions(Interpreter(table), tree):
        result = expr
    return result
