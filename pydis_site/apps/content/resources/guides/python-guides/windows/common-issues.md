---
title: Common Issues Using Python on Windows
description: A list of common issues with Python on Windows and how to fix them
icon: fab fa-windows
toc: 3
---

### When I run `python` in the terminal I get no result, or the Microsoft Store opens!

By default Windows has an alias for `python` in the terminal to guide you to install it from the [Microsoft
Store](https://apps.microsoft.com/store/search/python). We don't recommend installing Python from the Microsoft
Store, see why [here](../microsoft-store). To disable this alias, search "App execution aliases" in Windows search
and click on "Manage app execution aliases". In the list you should see two options with title "App Installer" and
descriptions `python.exe` and `python3.exe`. Disable both of them.

Note that if you are following instructions telling you to run a command starting with `python3`, those instructions are
intended for Unix/macOS systems. Try just using `python` instead.

If after doing this you have an issue with the Python command not being detected, see the question below.

### When I try and run my code with `python` in the terminal I get an error saying the command was not recognized

If you have not installed Python, you will need to do that. Follow our guide [here](../installing-and-using-python).

If you have installed python and are still having the issue, it is likely that you didn't check the "Add python.exe to
PATH" checkbox on the first page of the installer. See [our guide on adding Python to PATH](../putting-python-on-path)
for how to fix this. You can also use the `py` launcher instead of `python` by just replacing `python` in your command
with `py`. See [this guide](../installing-and-using-python/#the-py-launcher) for more information on that.

### I `pip` installed a package but when running my code I get a `ModuleNotFoundError`

-   #### Are you actually getting a `ModuleNotFoundError`?

    If you are using a code editor such as VSCode or PyCharm you may get a squiggly line under your import saying the
    module couldn't be found, it is possible that this is just an mistake by the editor, so try to actually run your
    code the way it is to ensure that it actually errors.

    If your code runs fine, you could try restarting your editor. If you have newly installed a module it may just not
    have detected it yet. If that doesn't help, you may need to configure your editor to ensure it is looking for the
    module in the correct Python environment. See [our guide on virtual
    environments](../installing-and-using-python/#virtual-environments) for more information.

-   #### Was the install successful?

    Look out for errors when installing the module you want. If you get an error, that's probably why the import isn't
    working, so you should look into it. Often a Google search of the relevant error text will help.

-   #### Did you use the correct module name?

    Double check that you haven't made a typo in the name you are importing, or in what you installed from
    [PyPI](https://pypi.org/), you need to make sure you type the name exactly as it should be.

    Also, **the name you should `import` may not be the same as the name you `pip install`**. Check the module's
    documentation or PyPI page if you are unsure. Examples of this are:

    -   [**opencv-python**](https://pypi.org/project/opencv-python/): You need to `pip install opencv-python`, but the
        import has to be `import cv2`
    -   [**discord.py**](https://pypi.org/project/discord.py/): You need to `pip install discord.py`, but the import has
        to be `import discord`
    -   [**python-dotenv**](https://pypi.org/project/python-dotenv/): You need to `pip install python-dotenv`, but the
        import has to be `import dotenv`
    -   [**Pillow**](https://pypi.org/project/Pillow/): You need to `pip install Pillow`, but the import is
        usually `from PIL import Image`.

    Normal imports in Python can't have hyphens (`-`) in them as it would be interpreted as subtraction. So if the
    package name has a `-` in it the import will definitely be different.

-   #### Are you installing to the same environment you're running your code from?

    This is a very common issue. When you install a module from PyPI, you will install it into a single Python
    environment, the one that the `pip` you invoked is part of. This could be different to the one you are running the
    script from if it's using a different Python installation, or a [virtual environment](../installing-and-using-python/#virtual-environments).

    You can tell when you're in a virtual environment because the name of the venv folder will usually be shown in
    parentheses at the start of terminal prompts. You can type `deactivate` to get out of it.
    [![Venv terminal prompt.](/static/images/content/python-on-windows/venv_prompt.png)](/static/images/content/python-on-windows/venv_prompt.png)

    ##### I'm using PyCharm

    > PyCharm creates a virtual environment for each project by default, so if you're installing a module using Pycharm
    > you need to make sure you also run your code through PyCharm. This also applies the other way round, if you want
    > to use a module in PyCharm you need to install it through PyCharm.
    >
    > You can see the exact path of the current Python interpreter, and thus virtual environment, in PyCharm by hovering
    > your mouse over the interpreter info menu on the bottom right:
    > [![PyCharm python.exe info.](/static/images/content/python-on-windows/pycharm_python_path.png)](/static/images/content/python-on-windows/pycharm_python_path.png)
    >
    > It's also possible to change PyCharm to use your system environment, see [their guide on configuring your
    > interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html) for more information.

    ##### I installed the module using pip from the command line

    > Run `pip -V` and look at the path it returned, which should be in the form
    > `<PATH_TO_PYTHON>\Lib\site-packages\pip`.
    >
    > Then put `import sys;print(sys.executable);sys.exit(0);` at the top (above imports!) of your python file, and run
    > it. The result should be in the form `<PATH_TO_PYTHON>\python.exe`.
    >
    > Now compare that `PATH_TO_PYTHON` to the one from `pip -V`. If they're different, this is the cause of the
    > `ModuleNotFoundError`. Follow the relevant "I'm running my code with ..." section below for how to fix this.

    ##### I'm running my code with `python` from the terminal.

    > If you are using a virtual environment, ensure you have activated it before running `pip install`. You can test
    > this by running `pip -V` and checking the path is the one of your virtual environment.
    >
    > Alternatively, you can use the `py` command to specify the python version you want to pip install into, e.g.
    > `py -3.9 -m pip install numpy`, and to specify the executable you want to run your code with, e.g.
    > `py -3.9 my_script.py`.
    >
    > If your `pip` and `python` commands are referring to different python environments at the same time, it's possible
    > your PATH is configured incorrectly. See our [guide for adding Python to PATH](../putting-python-on-path) for
    > how to fix this.

    ##### I'm running my code with the button in VSCode

    > To run your code from the same environment you installed Python to, set the VSCode Python interpreter to the one
    > at the path you found when running `pip -V` by following [this
    > guide](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment) (basically
    > `Ctrl+Shift+P -> Python: Select Interpreter -> select the one desired`). The path should be in the form
    > `PATH_TO_PYTHON\python.exe`
    >
    > Alternatively, you can pip install to the currently activated environment. If you have configured VSCode to use a
    > virtual environment, it should automatically activate it when you open a new terminal, so running the
    > `pip install` command in the VSCode terminal should work. If you are not using a virtual environment, you can use
    > the `py` launcher to specify the installation you want to install to.

### I `pip` installed a command line program but it isn't recognized

You pip installed a command line program like [`pyinstaller`](https://pypi.org/project/pyinstaller/) or
[`black`](https://pypi.org/project/black/) that is intended to be run from the command line, but it does not work. Two
common causes for this are:

-   You are using Python from the Microsoft Store ([which we don't recommend](../microsoft-store)).

    To check if this is the case, type `pip -V`. If the path output includes something like
    `PythonSoftwareFoundation.Python.3.10_3.10.2288.0_x64__qbz5n2kfra8p0`, you are using Python from the Microsoft
    Store. To fix this you will either have to use the full path to the scripts you want to use, or [uninstall the
    Microsoft Store Python](../microsoft-store/#uninstalling) and [install Python
    properly](../installing-and-using-python) with a [python.org installer](https://www.python.org/downloads).

-   You manually modified your PATH Environment Variable incorrectly

    If you added `Python` to PATH manually through environment variables, it is possible that you only added the
    executable but not the `\Scripts` folder. This would cause issues with `pip` and make command line tools not
    accessible. Look at our [guide on adding Python to the
    PATH](../putting-python-on-path/#advanced-method-manually-edit-the-path) for how to verify and fix this.

Projects that add a command line program usually work by adding an executable to the `\Scripts` folder of your Python
install (the full path of which is `C:\Users\<user>\AppData\Local\Programs\Python\Python311\Scripts` in a default 3.11
install). If you checked "Add python.exe to PATH" when installing Python, this folder will have been added to PATH, so
anything there should be runnable directly from the command line. Virtual environments also have their own `\Scripts`
directories that things can be installed to and are effectively on the PATH when the venv is properly activated.

### I get a `SyntaxError` when trying to run `pip`,`python`, or another command.

When you type `python` in the terminal you enter into the python REPL ([read-evaluate-print
loop](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)), also known as the Python console. This lets
you run `Python` code line by line without having to create a file. You also may have opened a Python REPL by clicking
on the Python App in your Start Menu.

General commands like `pip` and `python` should be run in your computer's normal terminal, that is, directly in
something like Command Prompt or PowerShell. _Not_ in the Python REPL, which usually has `>>>` at the start of each
line. To exit the Python REPL, type `exit()` and press enter. You should then be able to run your commands normally,
unless it was the Python App, in which case it will close completely and you'll need to open a normal terminal
separately.

### I tried to uninstall Python by deleting the folder, now it doesn't work and I can't reinstall it!

You should never uninstall your Python installation by deleting the folder it is in. If you have, you may need to edit
Registry Keys to fully remove the installation. Doing this is dangerous and beyond the scope of this guide.

To uninstall Python properly, run the installer for the version you want to uninstall and select "uninstall". If you no
longer have the installer, you can [re-download it from python.org](https://www.python.org/downloads/windows/) first.
