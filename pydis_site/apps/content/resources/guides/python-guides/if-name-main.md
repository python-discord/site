---
title: '`if __name__ == "__main__"`'
description: 'What is `if __name__ == "__main__"`, and why would you use it?'
---

You might see this structure in a Python file:

```py
# prog.py

def main_fn():
    # Put the main part of your program here.

if __name__ == "__main__":
    main_fn()
```

If the file is run directly (with `python prog.py` or `py prog.py`), it's called the main file of your program. In that case, our `main_fn()` function will be run.  If instead the file is imported by another file, then `main_fn()` will not be run.

When Python runs your module (your file), it automatically sets the `__name__` special global variable to `"__main__"`. The other way to run your file is to import it in a larger program. In that case, `__name__` is instead set to the filename of your module minus the `.py` extension.


## Another Example

```py
# foo.py

print("spam")

if __name__ == "__main__":
    print("eggs")
```

If you run the above module `foo.py` directly, `__name__` will be equal to `"__main__"`, so  both `spam`and `eggs` will be printed. Now consider this next example:

```py
# bar.py

import foo
```

If you run this file, it will import foo, which executes the code in `foo.py`. Now in foo.py `__name__` will be equal to `"foo"`. First it will print `spam`, and then the `if` statement will be false, so `eggs` won't print.

Often the code in the `if __name__` clause is a call to a main function, but it can be any code that you want.  Some files simply put their main code there even if its dozens of lines.

If there is just a single function call in the `if __name__` clause, it's often called `main()`, but that name isn't special to Python. You can call any code you like. Many people use `main()` because it's a clear indication of what's going on.


## Why would I do this?

There are a few reasons for using this structure, mostly about having two different uses for the file, one if it's run directly, and a different one for when it's imported as part of a larger program.

The most common reason is your module is a library, but also has a special case where it can be run directly. Sometimes libraries have small utility or demonstration scripts provided in the `__main__` clause.

Even if you don't intend your file to be used in two different ways, the convention of `if __name__ == "__main__":` gives a clear indication to the reader that this is the main file of the program.


## Why not have a `main` keyword?

Python often uses so-called "dunder" names for special behavior. The global name `__name__` lets files know how they are being run: directly or imported. Other languages might have a special name for the main function. Python instead lets you write your own if statement using `__name__` to decide what code should run be as the main body.
