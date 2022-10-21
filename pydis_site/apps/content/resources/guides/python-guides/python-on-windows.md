---
title: Python on Windows
description: This guide explains how manage your Python installation(s) on Windows
---

## The py launcher
By default, Python installed on Windows using the online Python installer comes with the "py launcher". It is a command line tool you invoke using the `py` command.

It provides the very useful `py -0p` command. This lists the python versions you have installed, the output will look like this:

    C:\Users\username>py -0p
    Installed Pythons found by py Launcher for Windows
    -V:3.11          C:\Users\username\AppData\Local\Programs\Python\Python311\python.exe
    -V:3.10          C:\Users\username\AppData\Local\Programs\Python\Python310\python.exe
    -V:3.9 *         C:\Users\username\AppData\Local\Programs\Python\Python39\python.exe

The versions will be ordered from newest to oldest, and the `*` will indicate which version running `py` will call by default. This depends on the following requirements, and may not be the same version you get from running `python` (if you get any):

    If an exact version is not given, using the latest version can be overridden by
    any of the following, (in priority order):
    • An active virtual environment
    • A shebang line in the script (if present)
    • With -2 or -3 flag a matching PY_PYTHON2 or PY_PYTHON3 Environment variable
    • A PY_PYTHON Environment variable
    • From [defaults] in py.ini in your %LOCALAPPDATA%\py.ini
    • From [defaults] in py.ini beside py.exe (use `where py` to locate)


You can override which version is called by specifying the major and minor versions to used. For example, to invoke python 3.7, you could run `py -3.7`. You can then pass any arguments to `python` on top of that, for example `py -3.7 myscript.py` to run `myscript.py`, or `py -3.7 -m pip install numpy` to invoke `pip` to install numpy into that version.

You can use `py` instead of `python` and not have any python versions on path at all. I would recommend having your "main" python version on path so you can invoke it with `python` if you want to, and then use `py` whenever you want a different version. The full documentation of the `py launcher` can be found [here](https://docs.python.org/3/using/windows.html#python-launcher-for-windows)

## Virtual Environments

Virtual environments, (aka `venvs`), are a way of letting each of your projects run in it's own python environment, different projects can have different versions of the same dependencies. This means that a `pip install` to your main Python will not affect a project where you're using a virtual environment.

You can follow this guide for information on how to create and activate a virtual environment: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment

If your editor/IDE has handling for venvs, it's worth looking into how it works. Here's a [VSCode tutorial](https://code.visualstudio.com/docs/python/environments), and here's [one for Pycharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html). [Poetry](https://python-poetry.org/) and [Pipenv](https://pipenv.pypa.io/en/latest/) are both popular tools for managing dependencies and virtual environments.


## Changing PATH
PATH is the system variable that Windows uses to locate executables needed on the command line. Whenever you type a command name in your terminal, for example `python` or `pip`, the terminal will look it up in the PATH to try and find out what executable that command refers to, so it can be run.

The Python installer does not add `python` to your PATH by default, but even if you forgot to add it when installing, it is easy to change.

### The safe method: through the installer

The easiest and and safest way to add Python to PATH is through the installer. Here is how to do that:

1. Search for "Apps and features" in the Windows Search Bar.
2. In the "App list" search bar search for "Python":
3. Find the version you want to add to PATH, click the three dots next to the name, and select "modify". This should open the installer window.
4. Select "Modify", and then click "next" on the "Optional Features" screen.
5. On the "Advanced Options" screen, tick the "Add Python to environment variables" checkbox:

    ![NkeEczCt2U](https://user-images.githubusercontent.com/22353562/126303895-60155ea5-7189-4924-9aa7-de696ca02ae9.png)

6. Click install.

Python should now be on your PATH! You will need to restart any terminals/editors you have open before they detect the change.

### The advanced method: editing environment variables

If you no longer have the installer, or want more control over variables in PATH, you can edit the environment variables manually.

First, search "environment variables" in Windows search and click on "Edit the system environment variables".  Then click the "Environment Variables" button near the bottom of the window.

Now there should be two boxes, one for user environment variables and one for system environment variables. There should be a "Path" entry under both. If you installed Python for your user account only (the default), double click the "Path" entry under the "User variables for [username]" section.

You should now see a list of paths. Each path represents a folder that will be searched for executables when looking up a command name in the terminal. The paths are searched from top to bottom, and the first executable found matching the name will be used. The system PATH variable has priority over the user one.

#### Python in the PATH

As there are different ways of installing Python it can appear in your PATH in different ways.

##### Adding Python to your PATH

First you will need to find the location of your Python executable. You can find this by running `py -0p` on the command line and selecting the path you want, or by adding `import sys;print(sys.executable)` to your code and running that.

For a standard Python install the file path should look something like `C:\Users\username\AppData\Local\Programs\Python\Python3xx\python.exe`. To add this two the path you should add two folders, the one containing `python.exe`, and the `Scripts/` directory in that directory. In this case the two paths would be:
- C:\Users\username\AppData\Local\Programs\Python\Python3xx\
- C:\Users\username\AppData\Local\Programs\Python\Python3xx\Scripts

It is important that both paths are added, otherwise `pip` and other commands will not work correctly.
