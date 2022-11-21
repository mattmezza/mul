mul
===

`mul` (my useless language) is a useless, interpreted programming language. 
I created it to learn more about programming languages without any 
utility expectation whatsoever.

It features:
- dynamic, strong typing
- lambda functions
- functional paradigm
- easy to write interpreter (≈26Kb/742 LOC of python)
- REPL

# Hello, world!
```
greeter = {:(who) print('Hello, ' + who + '!');};
greeter("world");
```

# Main characteristics

The implementation is in Python, but in the future I'd like to port it to 
a compiled language (maybe Rust).

The language is designed to be easy to write an interpreter for (therefore 
its uselessness).

`mul` is dynamically strongly typed.


# Types

There are just a few types baked into the language: `Boolean`, `Number`, `String` and `Function`.

## `Number`

No distinction between integer or float, everything is a number
```
num = 4.3;
another_num = 5;
```

Negative numbers are not supported (sorry). You can use the following:
```
negative_num = 0 - 4;
```

## `String`

Strings can be created with single or double quotes.

```
name = 'Matteo';
nickname = "mattmezza";
```

Strings can be concatenated with `+`.

## `Function`

Functions can be defined like so:
```
fullname = {
    fname = 'Matteo';
    lname = 'M';
    fname + lname;
};
```

The last expression is what the function will return when called. 
Functions can be called like so:
```
fullname();
```

Functions can have arguments defined as formal params like so:

```
fullname = {:(fname, lname)
    fname + lname;
};
```

As you would expect, such function can be called like so:
```
fullname('Matt', 'M');
```

# Control flow

There are no other constructs in the language (no `if`, no `for`, no `while`, 
etc...). In order to make the language a little bit more useful, such 
constructs are implemented in a native way in the form of a function.

For instance, there is an `if` function that you can use like so:
```
if(boolean, function, function_else);
```

# Comments

Single line comments are allowed by prepending the comment text with a `#`.

```
# this is a comment
a = 5;  # this is a comment too
```

# The standard library

A very small `std` has been built so far. It includes things like:

- `list` a pair based list implementation
- `logic` things like `and`, `or`, `all`, etc...
- `operator` functions like `sum`, `sub`, `mul`, `div`, etc...

The `std` lib is extremely sparse and unstructured, beware.


## Native hooks implementation

`mul` is implemented via native function call hooks that make it possible to 
export host language feature to `mul` itself (as done for the `if` function).

Native hooks implementation can be leveraged to quickly fill holes in the 
`std` lib.


# Tooling

There is no executor at the moment (altough creating one can be done quite 
easily). There is a `REPL` interface though:

```
$ python -m mul
> a = 5;
Type.NUM
5.0
```

`ctrl+d` quits the `REPL`.


# Examples

```
pow =
{:(b, e)
   if(equals(0, e), {1;}, {
        pow(b, e - 1) * b;
   });
};
print(pow(2, 3));  # prints 8
```

```
true = {1;};
false = {0;};
not = {:(v) if(v, false, true);};
and = {:(a,b) if(a, {if(b, true, false);}, false);};
or = {:(a,b) if(a, true, {if(b, true, false);});};
le = {:(v1, v2) if(or(lt(v1, v2), equals(v1, v2)), true, false);};
ge = {:(v1, v2) if(or(gt(v1, v2), equals(v1, v2)), true, false);};
```

For more examples, browse through the [std](https://github.com/mattmezza/mul/tree/main/std) lib.


# Installation

`mul` is currently not installable via any pkg manager. If you want to play 
with it, you'll have to clone the repo. It works with `python3.11.0rc2`, but 
it should also work with lower versions of `python3`.


# Contributing

I don't know if I will have time to review PRs and contributions but you can 
have fun with the language and maybe port it to other host languages. If you 
do, let me know, I'm a sucker for programming languages and I would enjoy 
checking out what you did.
