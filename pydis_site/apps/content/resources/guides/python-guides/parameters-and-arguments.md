---
title: Function Parameters and Arguments in Python
description: An in-depth look at function parameters and arguments, and how to use them.
---

A Python function is utilised in two steps:

1. The function definition/signature (used just once).
2. The function invocation/call (used many times).

The function definition uses parameters, whereas the function call uses arguments:

```python
def foo(this_is_a_parameter):
    print(this_is_a_parameter)
    
foo(this_is_an_argument)
```

An important detail to be aware of is that by default any argument used to call a function in Python can be used as both a positional and a keyword argument—just not at the same time.
A function call may contain a mixture of positional and keyword arguments, and—unless otherwise specified—an argument can reference the parameters in the function definition positionally, or by name (keyword).

# Positional Arguments

```python
def foo(a, b, c):
    print(a, b, c)
    
>>> foo(1, 2, 3)
1 2 3
```

In the above function definition we have three parameters `a`, `b`, and `c`.

When we invoke the function with the arguments `1`, `2`, and `3`, the function will map these values in the exact order given to the parameters in the function definition.
With no keyword reference given they become positional arguments.

# Keyword Arguments

```python
def foo(a, b, c):
    print(a, b, c)

>>> foo(1, 2, 3)
1 2 3

>>> foo(c=3, b=2, a=1)
1 2 3
```

As you can see, `foo(1, 2, 3)` and `foo(c=3, b=2, a=1)` are identical.
Referencing a function parameter by its name means that we are using a keyword argument.
The order in which keyword arguments are given does not matter.

# Mixing Positional and Keyword Arguments

So what happens if we want to mix the positional argument mapping with keyword arguments?

Python prioritises the mapping of positional arguments to their parameter names before the mapping of keywords.

```python
def foo(a, b, c):
    print(a, b, c)

>>> foo(1, c=3, b=2)
1 2 3
```

Passing a keyword argument using the name of a parameter that has already been given will not work:

```python
>>> foo(1, 2, a=3)
TypeError: foo() got multiple values for argument 'a'

>>> foo(1, b=2, b=3)
SyntaxError: keyword argument repeated
```

Attempting to pass positional arguments after a keyword argument will also not work:

```python
>>> foo(a=1, 2, 3)
SyntaxError: positional argument follows keyword argument
```

# Default Parameter Values

Although the syntax is similar, these are not to be confused with keyword arguments.  
Default parameter values appear within the function definition and allow us to conveniently set a default value. This means that if any argument is omitted, its default value will be used as the argument.

```python
def foo(a=0, b=0, c=0):
    print(a, b, c)

>>> foo()
0 0 0

>>> foo(1, 2, 3)
1 2 3

>>> foo(c=3, b=2)
0 2 3

>>> foo(1, c=3)
1 0 3
```

Using default parameter values does not change how a function can be invoked with arguments:

```python
>>> foo(1, 2, a=3)
TypeError: foo() got multiple values for argument 'a'

>>> foo(1, b=2, b=3)
SyntaxError: keyword argument repeated

>>> foo(a=1, 2, 3)
SyntaxError: positional argument follows keyword argument
```

You must specify any parameters without a default value before those with default values:

```python
def foo(a=0, b):
        ^
SyntaxError: non-default argument follows default argument
```

# Positional-only Parameters
[Python 3.8](https://docs.python.org/3/whatsnew/3.8.html#positional-only-parameters) / [PEP 570](https://www.python.org/dev/peps/pep-0570/) introduces the possibility to specify which parameters are required to be positional-only via a bare `/` parameter within a function definition.

```python
def foo(a=0, b=0, /, c=0, d=0):
    print(a, b, c, d)
```

The parameters defined before the bare `/` are now considered to be positional-only and keyword mapping will no longer work on them.  
In the above function definition `a` and `b` are now positional-only parameters.

These function calls will still work:

```python
>>> foo()
0 0 0 0

>>> foo(1)
1 0 0 0

>>> foo(1, 2, 3, 4)
1 2 3 4

>>> foo(1, 2, d=4, c=3)
1 2 3 4

>>> foo(1, d=4, c=3)
1 0 3 4

>>> foo(c=3, d=4)
0 0 3 4
```

However, attempting to pass keyword arguments for `a` or `b` will fail:

```python
>>> foo(1, b=2, c=3, d=4)
TypeError: foo() got some positional-only arguments passed as keyword arguments: 'b'
```

### Q: Why is this useful?

#### Keyword Argument Freedom

Passing a keyword argument using the name of a parameter that has already been given will not work.
This becomes an issue if we require keyword arguments that use the same parameter names as defined in the function signature, such as via callback functions.

```python
def foo(a, **kwargs):
    print(a, kwargs)

>>> foo(a=1, a=2)
SyntaxError: keyword argument repeated

>>> foo(1, a=2)
TypeError: foo() got multiple values for argument 'a'
```

#### Backwards Compatibility

Because Python allows that an argument by default can be either positional or keyword, a user is free to choose either option.
Unfortunately, this forces the author to keep the given parameter names as they are if they wish to support backwards compatibility, as changing the parameter names can cause dependent code to break.
Enforcing positional-only parameters gives the author the freedom to separate the variable name used within the function from its usage outside of it.

```python
def calculate(a, b):
    # do something with a and b

>>> calculate(1, 2)
```

A user could call this function using `a` or `b` as keywords, which the author may have not intended:

```python
>>> calculate(a=1, b=2)
```

However, by using `/`, the user will no longer be able to invoke using `a` or `b` as keywords, and the author is also free to rename these parameters:

```python
def calculate(x, y, /):
    # do something with x and y

>>> calculate(1, 2)
```

# Keyword-only Parameters

Similarly to enforcing positional-only parameters, we can also enforce keyword-only parameters using a bare `*` parameter.
The parameters defined after the bare `*` are now considered to be keyword-only.

```python
def foo(a=0, b=0, /, c=0, *, d=0):
    print(a, b, c, d)
    
>>> foo()
0 0 0 0

>>> foo(1, 2, 3)
1 2 3 0

>>> foo(1, 2, d=4, c=3)
1 2 3 4

>>> foo(1, d=4, c=3)
1 0 3 4
```

Although `c` can be either a positional or keyword argument, if we attempt to pass `d` as a non-keyword argument, it will fail:

```python
>>> foo(1, 2, 3, 4)
TypeError: foo() takes from 0 to 3 positional arguments but 4 were given
```
 
At least one named parameter must be provided after a bare `*` parameter. 
Writing a function definition similar to what is shown below would not make sense, as without the context of a named parameter the bare `*` can simply be omitted.

```python
def foo(a=0, *, **kwargs):
                ^
SyntaxError: named arguments must follow bare *
```
 
### Q: Why is this useful?

The main benefit of using keyword-only parameters is when they are used together with positional-only parameters to remove ambiguity.

However, it may sometimes also be desirable to use keyword-only arguments on their own.  
If we were to expose a function as part of an API, we may want the parameter names to carry explicit meaning.

Without using keyword names when invoking the function it can be unclear as to what the  provided arguments are for.
Additionally, a user could also choose to interchange positional arguments with keyword arguments, which can potentially add to the confusion.

```python
def update(identity=None, name=None, description=None):
    # handle the parameters
    
>>> update("value 1", "value 2", "value 3")

>>> update(1234, "value 1", description="value 2")
```

Enforcing the keyword names is clearer, as it carries context without needing to look at the function definition:

```python
def update(*, identity=None, name=None, description=None):
    # handle the parameters
    
>>> update(identity=1234, name="value 1", description="value 2")
```

# Summary

* Unless otherwise specified, an argument can be both positional and keyword.
* Positional arguments, when provided, must be in sequence.
* Positional arguments must be used before keyword arguments.
* Keyword arguments may be in any order.
* A default parameter value is used when the argument is omitted.
* A bare `/` used as a parameter in a function definition enforces positional-only parameters to its left.
* A bare `*` used as a parameter in a function definition enforces keyword-only parameters to its right.
