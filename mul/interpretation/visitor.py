from typing import Protocol, Tuple, Union, cast

from .. import ast
from .activation_record import Fn, Return


class Visitor(Protocol):
    def num(self, tree: ast.Num) -> Return:
        ...

    def str(self, tree: ast.Str) -> Return:
        ...

    def op_diadic(self, tree: ast.OpDiadic) -> Return:
        ...

    def sym(self, tree: ast.Sym) -> Return:
        ...

    def fn(self, tree: ast.Fn) -> Fn:
        ...

    def seq(self, tree: ast.Seq) -> Tuple[Union[Return, Fn, Tuple[str]]]:
        ...

    def call(self, tree: ast.Call) -> Return:
        ...

    def params(self, tree: ast.Params) -> Tuple[str]:
        ...

    def assignment(self, tree: ast.Assignment) -> Return:
        ...

    def visit(self, tree: ast.AST) -> Union[Return, Tuple[str], Fn]:
        if tree.is_a(ast.Seq):
            return self.seq(cast(ast.Seq, tree))
        elif tree.is_a(ast.Num):
            return self.num(cast(ast.Num, tree))
        elif tree.is_a(ast.Str):
            return self.str(cast(ast.Str, tree))
        elif tree.is_a(ast.Sym):
            return self.sym(cast(ast.Sym, tree))
        elif tree.is_a(ast.OpDiadic):
            return self.op_diadic(cast(ast.OpDiadic, tree))
        elif tree.is_a(ast.Params):
            return self.params(cast(ast.Params, tree))
        elif tree.is_a(ast.Fn):
            return self.fn(cast(ast.Fn, tree))
        elif tree.is_a(ast.Call):
            return self.call(cast(ast.Call, tree))
        elif tree.is_a(ast.Assignment):
            return self.assignment(cast(ast.Assignment, tree))
        else:
            raise Exception(f"Invalid tree '{type(tree)}'.")
