from pathlib import Path

from .interpretation import FnNative, Return, SymTable, interpret
from .lexer import lex
from .parser import parse


def char_at(table: SymTable, num: Return, s: Return) -> Return:
    if s.type != Return.Type.STR:
        raise Exception("char_at() must take a string as its second argument.")
    if num.type != Return.Type.NUM:
        raise Exception("char_at() must take a number as its first argument.")
    n = int(num.val)
    if n < 0 or n >= len(s.val):
        return Return.none()
    else:
        return Return.str(s.val[n])


def concat(table: SymTable, s1: Return, s2: Return) -> Return:
    if s1.type != Return.Type.STR or s2.type != Return.Type.STR:
        raise Exception(
            "concat() must take two strings as its arguments, "
            f"not '{s1}, {s2}'."
        )
    return Return.str(s1.val + s2.val)


def equals(table: SymTable, val1: Return, val2: Return) -> Return:
    return Return.num(1 if val1.val == val2.val else 0)


def lt(table: SymTable, val1: Return, val2: Return) -> Return:
    return Return.num(1 if val1.val < val2.val else 0)


def gt(table: SymTable, val1: Return, val2: Return) -> Return:
    return Return.num(1 if val1.val > val2.val else 0)


def if_(
    table: SymTable, cond: Return, then_fn: Return, else_fn: Return
) -> Return:
    if cond.type != Return.Type.NUM:
        raise Exception(
            f"Only numbers may be passed to an if, but I was passed '{cond}'."
        )
    to_call = then_fn if cond.val != 0 else else_fn
    return next(iter(interpret((to_call.val.body,), table)))


def len_(table: SymTable, ret: Return) -> Return:
    if ret.type != Return.Type.STR:
        raise Exception("len() can only be called for a string.")
    return Return.num(len(ret.val))


def print_(table: SymTable, ret: Return) -> Return:
    table.stdout().write(f"{ret.val}\n")
    return Return.none()


def _do_set(table: SymTable, name: str, value: Return):
    if name in table:
        table.put(name, value)
    elif table.has_parent():
        _do_set(table.parent, name, value)
    else:
        raise Exception(
            f"Attempted to set name '{name}' but it does not exist."
        )


def set_(table, symbol_name: Return, value: Return) -> Return:
    if symbol_name.type != Return.Type.STR:
        raise Exception(
            "set() takes a string as its first argument, "
            f"but was: '{symbol_name}'."
        )
    _do_set(table, symbol_name.val, value)
    return value


def include(name: str, table: SymTable) -> None:
    p = Path(__file__).parent.parent / Path(*name.split("/"))
    with open(p, "r", encoding="ascii") as f:
        interpret(parse(lex(f.read())), table)


def import_all(table: SymTable):
    table.put("char_at", FnNative(char_at).as_return())
    table.put("concat", FnNative(concat).as_return())
    table.put("equals", FnNative(equals).as_return())
    table.put("lt", FnNative(lt).as_return())
    table.put("gt", FnNative(gt).as_return())
    table.put("if", FnNative(if_).as_return())
    table.put("len", FnNative(len_).as_return())
    table.put("print", FnNative(print_).as_return())
    table.put("set", FnNative(set_).as_return())
    table.put("none", Return.none())

    include("std/logic.lang", table)
    include("std/str.lang", table)
    include("std/pair.lang", table)
    include("std/list.lang", table)
    include("std/operator.lang", table)
    include("std/test.lang", table)
