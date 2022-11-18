# flake8: noqa
import re
from typing import Iterable, cast

from . import tokens as T
from .lookahead import Lookahead


def _scan(first_char: str, chars: Lookahead[str], allowed: str) -> str:
    ret = first_char
    while (p := chars.peek()) is not None and re.match(allowed, p):
        ret += cast(str, chars.next())  # because chars.peek() is not None
    return ret


def _scan_string(delim: str, chars: Lookahead[str]) -> str:
    ret = ""
    while chars.peek() != delim:
        c = chars.next()
        if c is None:
            raise Exception("EOF")
        ret += c
    chars.next()
    return ret


def _scan_comment(chars: Lookahead[str]) -> None:
    while chars.peek() is not None and chars.peek() != "\n":
        chars.next()


def lex(program: str) -> Iterable[T.Token]:
    chars = Lookahead(program)
    while chars.peek() is not None:
        c = cast(str, chars.next())  # because chars.peek() is not None
        # fmt: off
        if c in " \n\t": pass
        elif c == "#": _scan_comment(chars)
        elif c == "(": yield T.LPar()
        elif c == ")": yield T.RPar()
        elif c == "{": yield T.LBrace()
        elif c == "}": yield T.RBrace()
        elif c == ",": yield T.Comma()
        elif c == ";": yield T.Semi()
        elif c == "=": yield T.Eq()
        elif c == ":": yield T.Colon()
        elif c == "+": yield T.Plus()
        elif c == "-": yield T.Min()
        elif c == "*": yield T.Mul()
        elif c == "/": yield T.Div()
        elif c in ("'", '"'): yield T.Str(_scan_string(c, chars))
        elif re.match("[.0-9]", c):
            yield T.Num(_scan(c, chars, "[.0-9]"))
        elif re.match("[_a-zA-Z]", c):
            yield T.Sym(_scan(c, chars, "[_a-zA-Z0-9]"))
        else: raise Exception(f"Invalid char '{c}'.")
        # fmt: on
