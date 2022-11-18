from __future__ import annotations

import fileinput
import itertools
import readline  # noqa: needed to make up arrow work in the REPL
import signal
import sys
from typing import Iterable

from . import exec, lex, lib, parse
from .interpretation import SymTable, pprint


def line() -> Iterable[str]:
    try:
        for char in input("> "):
            yield char
    except EOFError:
        sys.stdout.flush()
        sys.exit(0)


def repl(table: SymTable):
    signal.signal(signal.SIGINT, lambda s, f: ...)
    while True:
        try:
            for val in exec(line(), table):
                sys.stdout.write(str(val))
                sys.stdout.write("\n")
        except Exception as e:
            table.stderr().write(str(e))
            table.stderr().write("\n")
    table.stdout().write("\n")
    table.stdout().flush()


chars = itertools.chain.from_iterable


def main():
    glob_table = SymTable.root()
    if len(sys.argv) == 1:
        lib.import_all(glob_table)
        repl(glob_table)
    elif len(sys.argv) == 2:
        lib.import_all(glob_table)
        with fileinput.input() as f:
            exec(chars(f), glob_table)
    else:
        if sys.argv[2] in ("-t", "--tokens"):
            del sys.argv[2]
            with fileinput.input() as f:
                print(tuple(lex(chars(f))))
        elif sys.argv[2] in ("-a", "--ast"):
            del sys.argv[2]
            with fileinput.input() as f:
                pprint(parse(lex(chars(f))))
        else:
            print(
                f"Invalid opt flag '{sys.argv[2]}'. "
                "Should be one of (--tokens, --ast)."
            )
            print(f"e.g.: {sys.argv[0]} file.lang [-t|-a]")
            sys.exit(-1)


if __name__ == "__main__":
    sys.exit(main())
