---
title: Style Guide
description: Coding conventions for our Open Source projects.
icon: fab fa-python
---

> A style guide is about consistency.
> Consistency with this style guide is important.
> Consistency within a project is more important.
> Consistency within one module or function is the most important.

> However, know when to be inconsistent -- sometimes style guide recommendations just aren't applicable.
> When in doubt, use your best judgment. Look at other examples and decide what looks best. And don't hesitate to ask!

> — [PEP 8, the general Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

All of our projects have a certain project-wide style that contributions should attempt to maintain consistency with.
During PR review, it's not unusual for style adjustment requests to be commented.

We've added below a guideline to aid new contributors, allowing them to refer to it during development, to help get more familiar and to hopefully lessen some of the frustrations that come from first-time contributions.

Anything that isn't defined below falls back onto the [PEP 8 guidelines](https://www.python.org/dev/peps/pep-0008/), so be sure to reference it also.

# Code Structure
## Maximum Line Length
Each project has specified their respective maximum line lengths.
Generally, we try to keep this at 100 or 120 characters, making our length longer than the typical 79 characters.

Most IDEs and smarter editors will use the lint settings we store in the project's `tox.ini` or `.flake8` file after you install the appropriate development packages, so should conflict with our suggested project rules.
If your editor does not have this ability but instead requires setting it manually, make sure to change it to the appropriate length specified in these files.

## Line Breaks
Avoid breaking a line far earlier than necessary, such as:

```py
array = [  # there was plenty of room on this line
    1, 2, 3,
    4, 5, 6
]
```

Try instead to make use of the space you're allowed to use appropriately:
```py
array = [1, 2, 3, 4, 5, 6]
```

Any line continuations must be indented a full level, i.e. 4 spaces. So don't do:
```py
def an_example_function_definition_that_is_kinda_long(
  variable_name_of_the_first_positional_argument,  # only 2 spaces on the indent
  variable_name_of_the_second_positional_argument  # same here
)
```

Do instead:
```py
def an_example_function_definition_that_is_kinda_long(
    variable_name_of_the_first_positional_argument,
    variable_name_of_the_second_positional_argument
)
```

### Bracket and Item Arrangement
In the case where items contained in brackets need to be broken across multiple lines, items should be dropped to a new line after the opening bracket with an additional level of indentation.
The closing bracket ends on it's own new line, on the same indentation level as the opening bracket.

Avoid doing:
```py
def long_function_name_that_is_taking_up_too_much_space(var_one, var_two, var_three,  # didn't drop a line after the brackets
                                                        var_four, var_five, var_six,
                                                        var_seven, var_eight):
    print(var_one)
```
```py
def long_function_name_that_is_taking_up_too_much_space(
        var_one,
        var_two,
        var_three,
        var_four,
        var_five,
        var_six,
        var_seven,
        var_eight):  # didn't drop the closing bracket to a new line
    print(var_one)
```

Instead the correct style is:
```py
def long_function_name_that_is_taking_up_too_much_space(
        var_one,
        var_two,
        var_three,
        var_four,
        var_five,
        var_six,
        var_seven,
        var_eight
):
    print(var_one)
```

## Imports
Our projects require correctly ordering imports based on the pycharm import order rules.
If you use Pycharm as your main IDE, you can also use the `CTRL+ALT+O` shortcut to automatically reorder your imports to the correct style.

There's three groups of imports which are defined in the following order:

- Standard library
- 3rd party
- Local

Each group must be ordered alphabetically, with uppercase modules coming before lowercase.
```py
from packagename import A, Z, c, e
```

Direct imports must be distinct, so you cannot do:
```py
import os, sys
```
Instead do:
```py
import os
import sys
```

Absolute referencing for local project modules are preferenced over relative imports.

Wildcard imports should be avoided.

# Strings
## Quote Marks
Preference is to use double-quotes (`"`) wherever possible.
Single quotes should only be used for cases where it is logical.
Exceptions might include:

- using a key string within an f-string: `f"Today is {data['day']}"`.
- using double quotes within a string: `'She said "oh dear" in response'`

Docstrings must use triple double quotes (`"""`).

## Docstrings
All public methods and functions should have docstrings defined.

### Line Structure
Single-line docstrings can have the quotes on the same line:
```py
def add(a, b):
    """Add two arguments together."""
    return a + b
```

Docstrings that require multiple lines instead keep both sets of triple quotes on their own lines:
```py
def exponent(base, exponent=2):
    """
    Calculate the base raised to the exponents power.

    Default is 2 due to a squared base being the most common usage at this time.
    """
    return a ** b
```

### Spacing
Functions and methods should not have an extra empty newline after the docstring.
```py
def greeting(name):
    """Build a greeting string using the given name."""
    return f"Welcome, {name}"
```

Class docstrings do require an extra newline.
```py
class SecretStuffCog(commands.Cog):
    """Handle the secret commands that must never been known."""

    def __init__(self, bot):
        ...
```

### Mood
Imperative mood and present tense usage is preferenced when writing docstrings.

Imperative mood is a certain grammatical form of writing that expresses a clear command to do something.

**Use:** "Build an information embed."<br>
**Don't use:** "Returns an embed containing information."

Present tense defines that the work being done is now, in the present, rather than in the past or future.

**Use:** "Build an information embed."<br>
**Don't use:** "Built an information embed." or "Will build an information embed."

# Type Hinting
Functions are required to have type annotations as per the style defined in [PEP 484](https://www.python.org/dev/peps/pep-0484/). Type hints are recognized by most modern code editing tools and provide useful insight into both the input and output types of a function, preventing the user from having to go through the codebase to determine these types.

A function with type hints looks like:
```python
def foo(input_1: int, input_2: dict[str, int]) -> bool:
    ...
```
This tells us that `foo` accepts an `int` and a `dict`, with `str` keys and `int` values, and returns a `bool`.

In previous examples, we have purposely omitted annotations to keep focus on the specific points they represent.

> **Note:** if the project is running Python 3.8 or below you have to use `typing.Dict` instead of `dict`, but our three main projects are all >=3.9.
> See [PEP 585](https://www.python.org/dev/peps/pep-0585/) for more information.
