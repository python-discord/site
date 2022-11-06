---
title: The py Launcher on Windows
description: Common commands and usage of the Windows "py" Python launcher
---

When you install Python on Windows fron

TODO!!! rewrite/rearrange to be all about the py command

## The py launcher

By default, Python installed on Windows using the online Python installer comes
with the "py launcher". It is a command line tool you invoke using the `py`
command, and helps you invoke a specific python version.

It provides the `py -0p` command. This lists the python versions you have
installed, the output will look like this:

    C:\Users\username>py -0p
    Installed Pythons found by py Launcher for Windows
    -V:3.11          C:\Users\username\AppData\Local\Programs\Python\Python311\python.exe
    -V:3.10          C:\Users\username\AppData\Local\Programs\Python\Python310\python.exe
    -V:3.9 *         C:\Users\username\AppData\Local\Programs\Python\Python39\python.exe

The versions will be ordered from newest to oldest, and the `*` will indicate
which version running `py` will call by default. This depends on the following
requirements, and may not be the same version you get from running `python` (if
you get any):

```text
If an exact version is not given, using the latest version can be overridden by
any of the following, (in priority order):
• An active virtual environment
• A shebang line in the script (if present)
• With -2 or -3 flag a matching PY_PYTHON2 or PY_PYTHON3 Environment variable
• A PY_PYTHON Environment variable
• From [defaults] in py.ini in your %LOCALAPPDATA%\py.ini
• From [defaults] in py.ini beside py.exe (use `where py` to locate)
```

You can override which version is called by specifying the major and minor
versions to used. For example, to invoke python 3.7, you could run `py -3.7`.
You can then pass any arguments to `python` on top of that, for example
`py -3.7 myscript.py` to run `myscript.py`, or `py -3.7 -m pip install numpy`
to invoke `pip` to install numpy into that version.

You can use `py` instead of `python` and not have any python versions on PATH at
all. I would recommend having your "main" python version on path so you can
invoke it with `python` if you want to, and then use `py` whenever you want a
different version. The full documentation of the `py launcher` can be found
[here](https://docs.python.org/3/using/windows.html#python-launcher-for-windows)
