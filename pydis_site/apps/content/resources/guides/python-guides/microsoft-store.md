---
title: Why not to install Python from the Microsoft Store
description: This guide explains the issues with using Python installed from the Microsoft Store
---

Microsoft provides a Python app on the Microsoft Store as an alternative to using the [Standard Installer](https://www.python.org/downloads/). We would recommend that you use the standard installer wherever possible.

Here are some common issues caused when using Python from the Microsoft Store:

* Any command line tools like `black` or `pyinstaller` won't work directly. This happens because they work by adding an executable to the `Scripts/` directory, which isn't added to PATH on the Microsoft Store version of Python.

* Some modules and scripts wont work with it because of restricted permissions. This is explained here: https://docs.python.org/3/using/windows.html#redirection-of-local-data-registry-and-temporary-paths

* `python.exe` isn't added to PATH, but `pip.exe` is. This makes it easy to have an inconsistent `pip` and `python`. The `pip` is under the `C:\Users\username\AppData\Local\Microsoft\WindowsApps` entry, which wouldn't obviously have anything python related in it. If you add your normal python install path below this one the `pip` will be overridden by the `WindowsApps` one but the `python` one wont as it's overwriting the app execution alias.

* The app execution alias behaviour is confusing. If you use the online installer and for get to tick the box to to add to path, when you try and use `python`, you either get no output or the windows store opens. This hides the command not found error which would have indicated that their install didn't work as expected.
