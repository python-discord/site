---
title: Python on Windows
description: This guide explains how to install Python properly on Windows, what can go wrong, and how to fix things if it does.
---

When working with Python installs on Windows, it can be easy to get into a mess. This guide explains how to install Python properly on Windows, what can go wrong, and how to fix things if it does.

## Installing Python

The recommended installation method on windows is to install it directly from the [Python website's Downloads page](https://www.python.org/downloads/). Installing Python from the Microsoft Store is not recommended as it can [cause issues](https://docs.python.org/3/using/windows.html#redirection-of-local-data-registry-and-temporary-paths).

### Which version?
**Recommended**: Second latest

Installing the latest version will give you access to Python's newest features. However, some modules may not support the newest versions straight away, so installing the second latest will help you avoid those issues.

If you find you want some newer features or your module does not support your current version, you can always install another version as well.

### 32-bit vs 64-bit?
**Recommended**: 64-bit

It is recommended that you install 64-bit python unless you have reason not to. With 32 bit you may run into memory limits if doing intensive operations (Python will be limited to using 4GB of memory), and some installed modules may not offer prebuilt wheels for 32 bit, potentially making installs slower or meaning you have to install build dependencies.

If you get an error when installing 64-bit Python, your computer may not support it. To find out if this is the case, search "About your PC" in windows search and open the settings page. Then look for the "System Type" option under "Device Specifications". It should say "64-bit operating system, x64-based processor" if you have support. You need a 64 bit processor and OS to install 64 bit programs.

### Add to PATH, or not?
**Recommended**: Yes, add to PATH

You should add the first Python version you install to PATH. This allows you to use the `python` and `pip` commands in your terminal to invoke Python. For subsequent versions you'll need to decide which version you want to be accessible with the `python` command. You can always specify which one you want using the #py-launcher

If you installed Python without adding to PATH and now want to add it, see (#changing-path)[#changing-path]

### Running the installer
When you run the installer you should see a screen like this:

![python_installer_screen](https://user-images.githubusercontent.com/22353562/126144479-cfe6bd98-6d2e-47c3-b6b3-5de9f2656e9a.png)

If you want to add to PATH, be sure to tick the "Add Python X.X to PATH" checkbox. Then click install, and wait for the install to finish!

To test your installation, type "cmd" in the windows search bar and select "Command Prompt" to open a terminal (make sure it's opened *after* installation has finished) type `python -V`, and press enter. If it outputs your python version, you've successfully installed Python. (if you didn't add to PATH, you can use the [#the-py-launcher](#the-py-launcher) to test instead)

## Using Python
### The py launcher
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

You can use `py` instead of `python` and not have any python versions on path at all, but personally I would recommend having your "main" python version on path so you can invoke it with `python` if you want to. The full documentation of the `py launcher` can be found [here](https://docs.python.org/3/using/windows.html#python-launcher-for-windows)

### Virtual Environments

Virtual environments, (aka `venvs`), are a way of letting each of your projects run in it's own python environment, different projects can have different versions of the same dependencies.

If your editor/IDE has handling for venvs, it's worth looking into how it works. Here's a [VSCode tutorial](https://code.visualstudio.com/docs/python/environments), and here's [one for Pycharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html). [Poetry](https://python-poetry.org/) and [Pipenv](https://pipenv.pypa.io/en/latest/) are both popular tools for managing dependencies.

### Changing PATH
PATH is the system variable that Windows uses to locate executables needed on the command line. Whenever you type a command name in your terminal, the terminal will look it up in the PATH to try and find out what executable that command refers to, so it can be run.

The Python installer does not add Python to path by default, but even if you forgot to add it when installing, it is easy to change.

#### The safe method: through the installer

Some tutorials would advise going into your environment variables and editing your PATH manually, however it can be done more easily and safely directly from the installer. Here is how to do that.

1. Search for "Apps and features" in the Windows Search Bar.
2. In the "App list" search bar search for "Python":
3. Find the version you want to add to PATH, click the three dots next to the name, and select "modify". This should open the installer window.
4. Select "Modify", and then click "next" on the "Optional Features" screen.
5. On the "Advanced Options" screen, tick the "Add Python to environment variables" checkbox:

    ![NkeEczCt2U](https://user-images.githubusercontent.com/22353562/126303895-60155ea5-7189-4924-9aa7-de696ca02ae9.png)

6. Click install.

Python should now be on your PATH! You may need to restart any terminals/editors you have open before they detect the change.

#### The advanced method: editing environment variables

If you no longer have the installer, or want more control over variables in PATH, you can edit the environment variables manually.

TODO: write guide.

## Common Issues

### When I run `python` in the terminal I get no result, or the Windows Store opens!

By default windows has an alias for Python to redirect you and try and get you to install it from the Windows Store. It is recommended to install Python using the online installers rather than the windows store.

To disable this alias, search "App execution aliases" in windows search and click on "Manage app execution aliases". In the list you should see two options with title "App Installer" and descriptions `python.exe` and `python3.exe`, disable them both.

Note that if you are following instructions telling you to run a command starting with `python3`, those instructions are intended for linux. Try just using `python` instead.

If after doing this you have an issue with the Python command not being detected but you have installed Python, see the below question.

### When I try and run my code with `python` in the terminal I get an error saying the command was not recognised

If you have not installed Python, you will need to do that. See #installing-python section.

If you have installed python and are still getting the error, it is most likely that you forgot to add to PATH when doing so. See #managing-path

You can also use the `py` launcher instead of `python` by just replacing `python` in your command with `py`. See #py-launcher for more information on this.

### I `pip` installed a package but when running my code get a `ModuleNotFoundError`

* ##### Are you actually getting a `ModuleNotFoundError`?

    If you are using a code editor such as VSCode or Pycharm you may get a squiggly line under your import saying the module couldn't be found, it is possible that this is just an mistake by the editor, so try running your code with to ensure if it actually errors.

    If your code runs fine, you could try restarting your editor - if you have newly installed a module it may just not have detected it yet. If that doesn't help, you may need to configure it to ensure it is looking for the module in the correct Python environment.

* ##### Was the install successful?

    Look out for errors when installing the module you want. If you get an error, that's probably why you can't install it, so you should look into it. Often a google search will help with this.


* ##### Did you use the correct module name?

    Double check that you haven't made a typo in the name you are importing, or in what you installed from PyPI, you need to make sure you get the name exactly as it should be.

    Also **the name you should `import` may not be the same as the name you `pip install`**. Check the module's docs or PyPI page if you are unsure.
    Examples of this are:

    * [**opencv-python**](https://pypi.org/project/opencv-python/): You need to `pip install opencv-python`, but the import has to be `import cv2`
    * [**discord.py**](https://pypi.org/project/discord.py/): You need to `pip install discord.py`, but the import has to be `import discord`
    * [**python-dotenv**](https://pypi.org/project/python-dotenv/): You need to `pip install python-dotenv`, but the import has to be `import dotenv`


* ##### Are you installing to the same environment you're running your code from?

    This is a very common issue. When you install a module from PyPI, you will install it into a single python executable, the one that the `pip` you invoked is referring to. This could be different to the one you are running the script from, usually because it's using a different python version, or a virtual environment.

    * ###### I installed the module using pip

        Run `pip -V` and look at the path returned it should be in the form `<PATH_TO_PYTHON>\Lib\site-packages\pip`.

        Then put `import sys;print(sys.executable);sys.exit(0)` at the top (above imports!) of your python file, and run it. The result should be in the form `<PATH_TO_PYTHON>\python.exe`.

        Now compare that `PATH_TO_PYTHON` to the one from `pip -V`. If they're different, this is the cause of the `ModuleNotFoundError`. See the relevant "I'm running with ..." sections below for how to resolve this.

    * ###### I installed the module using PyCharm

        PyCharm creates a virtual environment by default, so if you're installing the module using Pycharm you need to make sure you also run your code from Pycharm.

    How to fix it depends on how you're running your code

    * ###### I'm running my code with `python` from the terminal.

        If you are using a virtual environment, ensure you have activated your venv before running `pip install`

        * If you are running your code through your editor, make sure you have it set up to use the same editor you are `pip install`ing into.
        * Use the `py` command to specify the python version you want to pip install into, e.g. `py -3.9 -m pip install numpy`, or to specify.
        If you're still getting an error, the chances are you installed the module to a different environment to the one you're running python with. This is very common, and how best to fix it depends on what editor you're using.

    * ###### I'm running my code with PyCharm

        PyCharm creates a virtual environment for each project by default, so you need to make sure that virtual environment is activated before installing modules. The easiest way to do this is by `pip install`ing directly from the PyCharm editor terminal, where it will be activated by default.

        You can also use PyCharm's GUI to install modules.

    * ###### I'm running my code with VSCode

        To run your code from the same environment you installed Python to, set the interpreter to the one at the path you found when running `pip -V` by following [this guide](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment). The path should be in the form `PATH_TO_PYTHON\python.exe`

        Alternatively, you can pip install to the currently activated environment. If you have configured VSCode to use a virtual environment, it should automatically activate it when you open a new terminal, so running the `pip install` command in the VSCode terminal should work. If you are not using a virtual environment, you can use the `py` launcher to specify the installation you want to install to.

### I `pip` installed a command line program but it isn't recognised

If you pip installed a command line program like `PyInstaller` that is intended to be run from the command line, but it does not work, this suggests the Python installation you installed it to is not on `PATH` (or at least not fully).

Projects that add a command line program usually work by adding an executable to the `/Scripts` folder of your Python install. If you clicked "Add to PATH" when installing Python this folder will have been added to PATH, so anything there should be runnable directly from the command line. This should also be the case when using a virtual environment, as long as it is properly activated.

If you added `Python` to PATH manually through environment variables, it is possible that you only added the executable but not the `/Scripts` folder.

### I get a `SyntaxError` when trying to run `pip`,`python`, or another command.

When you type `python` in the terminal you enter into the python REPL (read-evaluate-print loop). This lets you run lines of `Python` code, like `print("Hello World")`, without having to create a file.

General commands like `pip` and `python` should be run in the terminal, not in the Python REPL. To exit the REPL, type `exit()` and press enter. You should then be able to run your commands normally.

### I tried to uninstall Python by deleting the folder, now it doesn't work and I can't reinstall it!

You should never uninstall your Python installation by deleting the folder it is in. If you have, you may need to edit Registry Keys to fully remove the installation. Doing this is dangerous and beyond the scope of this guide.

To uninstall Python properly, run the installer for the version you want to uninstall and select "uninstall". If you no longer have the installer, you can re-download it first.
