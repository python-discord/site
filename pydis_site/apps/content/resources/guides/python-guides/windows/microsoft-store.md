---
title: Why NOT to install Python from the Microsoft Store
description: This guide explains the issues with using Python installed from the Microsoft Store
---

Microsoft provides versions of Python for Windows
[on the Microsoft Store](https://apps.microsoft.com/store/search/python) as an alternative to using the
[full installer from python.org](https://www.python.org/downloads). **We recommend you install Python on Windows using the
[full installer from python.org](https://www.python.org/downloads),
and not from the Microsoft store wherever possible!**

You can follow [this guide to install Python from python.org](../install-on-windows.md) and more Python Windows releases
can be found [here](https://www.python.org/downloads/windows).

Here are some common issues with using Python from the Microsoft Store:

-   ##### Command line tools won't work

    Most command line tools, like [`black`](https://pypi.org/project/black/) or
    [`pyinstaller`](https://pypi.org/project/pyinstaller/), won't work directly (without specifying the full path, or
    invoking them as a module if they allow it). This happens because they normally work by adding an executable to the
    `\Scripts` directory, which isn't added to Path on the Microsoft Store version of Python.

-   ##### It can cause issues with permissions

    Some modules and scripts wont work with it because of restricted permissions.
    This is explained
    [in the Python documentation](https://docs.python.org/3/using/windows.html#redirection-of-local-data-registry-and-temporary-paths)

-   ##### It can cause Path confusion

    Path is the Windows environment variable that determine what programs run when you type commands in terminals.
    (Actually there are two Paths, a user one and a system one that has precedence, but they get [combined when
    used](https://superuser.com/a/878382/935845).) With Python from the Microsoft Store installed, your `python`, `py`,
    and `pip` commands may get mixed up with the python.org ones, depending on the order and contents of Path.

    The Path entry for the Microsoft Store is `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps`. The entries for the
    full python.org install are commonly `C:\Users\<user>\AppData\Local\Programs\Python\Python311` and
    `C:\Users\<user>\AppData\Local\Programs\Python\Python311\Scripts` (for Python 3.11). If for some reason you want
    both installed, put the ones you want the commands for higher up in Path.

-   ##### Confusing app execution alias behaviour

    Typing `python` into a terminal when it is not already installed or not properly on Path may open up the Microsoft
    Store to the Python app, pushing you to install it and confusingly hiding the command not found error that would
    normally happen.

    You can change this behavior by searching "Manage app execution aliases" in the Start menu and toggling off "App
    Installer" for python.exe and python3.exe.

-   #### You can't specify or easily see the patch version

    The Microsoft Store Python versions are listed simply like 3.10 rather than 3.10.8 even though it may be 3.10.8
    under the hood. It's uncommon, but if you know you need a different patch version ([aka micro
    version](https://peps.python.org/pep-0440/#final-releases)), e.g. 3.10.7, you'll need to [install from
    python.org](https://www.python.org/downloads/windows/).

If you have the Microsoft Store version of Python and want to uninstall it, you can search "uninstall" in the Start menu
to open up the "Apps & features" settings and filter by "python". The Python app that has a console in the icon and
"Python Software Foundation" under the name is the Microsoft Store one (see image below). Click it and hit Uninstall.

![Which version is which when uninstalling Python](/static/images/content/python-on-windows/ms_store_uninstall.png)
