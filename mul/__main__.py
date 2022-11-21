import fileinput
import itertools
import readline  # noqa: needed to make up arrow work in the REPL
import signal
import sys
from typing import Iterable

from . import Interpreter, lex, parse
from .interpretation import pprint


def line() -> Iterable[str]:
    try:
        for char in input("> "):
            yield char
    except EOFError:
        sys.stdout.flush()
        sys.exit(0)


def repl(interpreter: Interpreter):
    signal.signal(signal.SIGINT, lambda s, f: ...)
    while True:
        try:
            for val in interpreter.eval(line()):
                sys.stdout.write(str(val))
                sys.stdout.write("\n")
        except Exception as e:
            interpreter.env.stderr().write(str(e))
            interpreter.env.stderr().write("\n")
    interpreter.env.stdout().write("\n")
    interpreter.env.stdout().flush()


chars = itertools.chain.from_iterable


def main():
    interpreter = Interpreter.with_std()
    if len(sys.argv) == 1:
        repl(interpreter)
    elif len(sys.argv) == 2:
        with fileinput.input() as f:
            interpreter.eval(chars(f))
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
