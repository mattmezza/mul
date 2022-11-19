mul
===

`mul` (my useless language) is a useless, interpreted programming language. 
I created it to learn more about programming languages without any 
utility expectation whatsoever.

## Main characteristics

The implementation is in Python, but in the future I'd like to port it to 
a compiled language (maybe Rust).

The language is designed to be easy to write an interpreter for (therefore 
its uselessness).

`mul` is dynamically strongly typed.

### Types

There are just a few types baked into the language: `Boolean`, `Number`, `String` and `Function`.

#### `Number`

No distinction between integer or float, everything is a number
```
num = 4.3;
another_num = 5;
```

Negative numbers are not supported (sorry). You can use the following:
```
negative_num = 0 - 4;
```

#### `String`

Strings can be created with single or double quotes.

```
name = 'Matteo';
nickname = "mattmezza";
```

Strings can be concatenated with `+`.

#### `Function`

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

### Control flow

There are no other constructs in the language (no `if`, no `for`, no `while`, 
etc...). In order to make the language a little bit more useful, such 
constructs are implemented in a native way in the form of a function.

For instance, there is an `if` function that you can use like so:
```
if(predicate, function, function_else);
```
