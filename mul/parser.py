from dataclasses import dataclass
from typing import Iterable, Self, Sequence, Tuple, cast

from . import ast
from . import tokens as T
from .lookahead import Lookahead


@dataclass(frozen=True)
class Parser:
    tokens: Lookahead[T.Token]
    stop_at: Sequence[T.Token]

    def next(self: Self, prev: ast.AST | None) -> ast.AST | None:
        self.fail_if_at_end(T.Semi())
        token = cast(T.Token, self.tokens.peek())
        if token in self.stop_at:
            return prev
        self.tokens.next()
        if token.is_a(T.Num) and prev is None:
            return self.next(ast.Num(float(cast(T.Num, token).val)))
        elif token.is_a(T.Str) and prev is None:
            return self.next(ast.Str(cast(T.Str, token).val))
        elif token.is_a(T.Sym) and prev is None:
            return self.next(ast.Sym(cast(T.Sym, token).val))
        elif token.is_a(T.Plus):
            nxt = cast(ast.AST, self.next(None))
            return self.next(ast.OpDiadic.sum(cast(ast.AST, prev), nxt))
        elif token.is_a(T.Min):
            nxt = cast(ast.AST, self.next(None))
            return self.next(ast.OpDiadic.min(cast(ast.AST, prev), nxt))
        elif token.is_a(T.Mul):
            nxt = cast(ast.AST, self.next(None))
            return self.next(ast.OpDiadic.mul(cast(ast.AST, prev), nxt))
        elif token.is_a(T.Div):
            nxt = cast(ast.AST, self.next(None))
            return self.next(ast.OpDiadic.div(cast(ast.AST, prev), nxt))
        elif token.is_a(T.LPar):
            args: ast.Seq = self.exprs(T.Comma(), T.RPar())
            return self.next(ast.Call(cast(ast.Sym, prev), args))
        elif token.is_a(T.LBrace):
            params: ast.Params = self.params()
            body: ast.Seq = self.exprs(T.Semi(), T.RBrace())
            return self.next(ast.Fn(params, body))
        elif token.is_a(T.Eq):
            if prev is None or prev.is_a(ast.Sym) is False:
                raise Exception(f"Cannot assign to '{type(prev)}'.")
            nxt: ast.AST = self.next(None)
            return self.next(ast.Assignment(cast(ast.Sym, prev), nxt))
        else:
            raise Exception(f"Unexpected token {token}.")

    def params(self) -> ast.Params:
        token = self.tokens.peek()
        if token is None:
            raise Exception("EOF in function definition.")
        if token.is_a(T.Colon) is False:
            return ast.Params(tuple())
        self.tokens.next()
        self.fail_if_at_end(T.LPar())
        token = cast(T.Token, self.tokens.peek())
        if token.is_a(T.LPar) is False:
            raise Exception("':' must be followed by '(' in a fn def.")
        self.tokens.next()
        seq = self.exprs(T.Comma(), T.RPar())
        for tree in seq:  # type:ignore
            if isinstance(tree, ast.Sym) is False:
                raise Exception(f"Invalid symbol '{type(tree)}' in fn def.")
        return ast.Params(cast(Tuple[ast.Sym, ...], seq.children))

    def exprs(self, sep: T.Token, end: T.Token) -> ast.Seq:
        seq = ast.Seq(())
        self.fail_if_at_end(end)
        token = cast(T.Token, self.tokens.peek())
        if token.is_a(type(end)):
            self.tokens.next()
        else:
            arg_parser = Parser(self.tokens, (sep, end))
            while token.is_a(type(end)) is False:
                p = arg_parser.next(None)
                if p is not None:
                    seq = seq.replace(children=seq.children + (p,))
                token = cast(T.Token, self.tokens.peek())
                self.tokens.next()
                self.fail_if_at_end(end)
        return seq

    def fail_if_at_end(self, expected: T.Token) -> None:
        if self.tokens.peek() is None:
            raise Exception(f"EOF while '{expected}' was expected.")


def parse(tokens: Iterable[T.Token]) -> Iterable[ast.AST]:
    parser = Parser(Lookahead(tokens), (T.Semi(),))
    while parser.tokens.peek() is not None:
        tree = parser.next(None)
        if tree is not None:
            yield tree
        parser.tokens.next()
