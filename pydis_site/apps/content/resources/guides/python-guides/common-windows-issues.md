---
title: Common issues using Python on Windows
description: This guide describes common issues you may run into when using Python on Windows and how to fix them.
---

### When I run `python` in the terminal I get no result, or the Windows Store opens!

By default Windows has an alias for `python` in the terminal to guide you to
install it from the Windows Store. We would not recommend that you install
Python from the Microsoft Store, see why [here](../microsoft-store.md).
To disable this alias, search "App execution aliases" in windows search and
click on "Manage app execution aliases". In the list you should see two options
with title "App Installer" and descriptions `python.exe` and `python3.exe`.
Disable both of them.

Note that if you are following instructions telling you to run a command
starting with `python3`, those instructions are intended for Unix/macOS systems.
Try just using `python` instead.

If after doing this you have an issue with the Python command not being
detected, see the below question.

### When I try and run my code with `python` in the terminal I get an error saying the command was not recognised

If you have not installed Python, you will need to do that. Follow our guide [here](../install-on-windows.md).

If you have installed python and are still getting the error, it is likely that
you forgot to add to PATH when doing so. See [our guide on adding Python to
PATH](../python-on-windows.md#changing-path) for how to fix this.
You can also use the `py` launcher instead of `python` by just replacing
`python` in your command with `py`. See
[this guide](../python-on-windows.md#the-py-launcher) for more information.

### I `pip` installed a package but when running my code get a `ModuleNotFoundError`

* #### Are you actually getting a `ModuleNotFoundError`?

    If you are using a code editor such as VSCode or Pycharm you may get a
    squiggly line under your import saying the module couldn't be found, it is
    possible that this is just an mistake by the editor, so try running your
    code with to ensure if it actually errors.

    If your code runs fine, you could try restarting your editor - if you have
    newly installed a module it may just not have detected it yet. If that
    doesn't help, you may need to configure it to ensure it is looking for the
    module in the correct Python environment.

* #### Was the install successful?

    Look out for errors when installing the module you want. If you get an
    error, that's probably why the import isn't working, so you should look
    into it. Often a google search will help with this.

* #### Did you use the correct module name?

    Double check that you haven't made a typo in the name you are importing, or
    in what you installed from PyPI, you need to make sure you get the name
    exactly as it should be.

    Also **the name you should `import` may not be the same as the name you `pip
    install`**. Check the module's docs or PyPI page if you are unsure. Examples
    of this are:

    * [**opencv-python**](https://pypi.org/project/opencv-python/): You need to
      `pip install opencv-python`, but the import has to be `import cv2`
    * [**discord.py**](https://pypi.org/project/discord.py/): You need to `pip
      install discord.py`, but the import has to be `import discord`
    * [**python-dotenv**](https://pypi.org/project/python-dotenv/): You need to
      `pip install python-dotenv`, but the import has to be `import dotenv`

* #### Are you installing to the same environment you're running your code from?

    This is a very common issue. When you install a module from PyPI, you will
    install it into a single python executable, the one that the `pip` you
    invoked is referring to. This could be different to the one you are running
    the script from, usually because it's using a different python version, or a
    virtual environment.

    * ###### I installed the module using pip

        Run `pip -V` and look at the path returned it should be in the form
        `<PATH_TO_PYTHON>\Lib\site-packages\pip`.

        Then put `import sys;print(sys.executable);sys.exit(0)` at the top
        (above imports!) of your python file, and run it. The result should be
        in the form `<PATH_TO_PYTHON>\python.exe`.

        Now compare that `PATH_TO_PYTHON` to the one from `pip -V`. If they're
        different, this is the cause of the `ModuleNotFoundError`. See the
        relevant "I'm running with ..." sections below for how to resolve this.

    * ###### I installed the module using PyCharm

        PyCharm creates a virtual environment by default, so if you're
        installing the module using Pycharm you need to make sure you also run
        your code from Pycharm.

    How to fix it depends on how you're running your code

    * ###### I'm running my code with `python` from the terminal.

        If you are using a virtual environment, ensure you have activated your
        venv before running `pip install`

        * If you are running your code through your editor, make sure you have
          it set up to use the same editor you are `pip install`ing into.
        * Use the `py` command to specify the python version you want to pip
        install into, e.g. `py -3.9 -m pip install numpy`, or to specify. If
        you're still getting an error, the chances are you installed the module
        to a different environment to the one you're running python with. This
        is very common, and how best to fix it depends on what editor you're
        using.

    * ###### I'm running my code with PyCharm

        PyCharm creates a virtual environment for each project by default, so
        you need to make sure that virtual environment is activated before
        installing modules. The easiest way to do this is by `pip install`ing
        directly from the PyCharm editor terminal, where it will be activated by
        default.

        You can also use PyCharm's GUI to install modules.

    * ###### I'm running my code with VSCode

        To run your code from the same environment you installed Python to, set
        the interpreter to the one at the path you found when running `pip -V`
        by following [this
        guide](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment).
        The path should be in the form `PATH_TO_PYTHON\python.exe`

        Alternatively, you can pip install to the currently activated
        environment. If you have configured VSCode to use a virtual environment,
        it should automatically activate it when you open a new terminal, so
        running the `pip install` command in the VSCode terminal should work. If
        you are not using a virtual environment, you can use the `py` launcher
        to specify the installation you want to install to.

### I `pip` installed a command line program but it isn't recognised

You pip installed a command line program like `PyInstaller` or `black` that is
intended to be run from the command line, but it does not work. Two common causes
for this are:

* You are using Python from the Microsoft Store

    To check if this is the case, type `pip -V`. If the path output includes
    something like
    `PythonSoftwareFoundation.Python.3.10_3.10.2288.0_x64__qbz5n2kfra8p0`, you
    are using Python from the Microsoft Store. To fix this you will either have
    to use the full path to the scripts you want to use, or uninstall the
    Microsoft Store Python and install Python properly with the online
    installer.

* You manually modified your PATH Environment Variable incorrectly

    If you added `Python` to PATH manually through environment variables, it is
    possible that you only added the executable but not the `/Scripts` folder.
    This would cause issues with `pip` and make command line tools not
    accessible. Look at our [guide on adding Python to the
    PATH](../python-on-windows.md#adding-python-to-your-path) for how to verify
    and fix this.

Projects that add a command line program usually work by adding an executable to
the `/Scripts` folder of your Python install. If you clicked "Add to PATH" when
installing Python this folder will have been added to PATH, so anything there
should be runnable directly from the command line. This should also be the case
when using a virtual environment, as long as it is properly activated.

### I get a `SyntaxError` when trying to run `pip`,`python`, or another command.

When you type `python` in the terminal you enter into the python REPL
(read-evaluate-print loop). This lets you run `Python` code line by line without
having to create a file.

General commands like `pip` and `python` should be run in the terminal, not in
the Python REPL. To exit the REPL, type `exit()` and press enter. You should
then be able to run your commands normally.

### I tried to uninstall Python by deleting the folder, now it doesn't work and I can't reinstall it!

You should never uninstall your Python installation by deleting the folder it is
in. If you have, you may need to edit Registry Keys to fully remove the
installation. Doing this is dangerous and beyond the scope of this guide.

To uninstall Python properly, run the installer for the version you want to
uninstall and select "uninstall". If you no longer have the installer, you can
re-download it first.
