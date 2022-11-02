---
title: Why not to install Python from the Microsoft Store
description: This guide explains the issues with using Python installed from the Microsoft Store
---

Microsoft provides a Python app on the Microsoft Store as an alternative to
using the [Standard Installer](https://www.python.org/downloads/). We would
recommend that you use the standard installer instead wherever possible.

Here are some common issues with using Python from the Microsoft Store:

* ##### Command line tools won't work
  Most command line tools, like `black` or `pyinstaller`, won't work directly
  (without specifying the full path, or invoking them as a module if they allow
  it). This happens because they work by adding an executable to the `Scripts/` directory,
  which isn't added to PATH on the Microsoft Store version of Python.

* ##### It can cause issues with permissions
  Some modules and scripts wont work with it because of restricted permissions.
  This is explained
  [in the Python documentation](https://docs.python.org/3/using/windows.html#redirection-of-local-data-registry-and-temporary-paths)

* ##### It uses PATH inconsistently
  `python.exe` isn't added to PATH, but `pip.exe` is. This makes it easy to have
  an inconsistent `pip` and `python`. The `pip` is under the
  `C:\Users\username\AppData\Local\Microsoft\WindowsApps` entry, which wouldn't
  obviously have anything Python related in it. If you add your normal Python
  install path below this one, it's `pip` will be overridden by the `WindowsApps`
  one but the `python` one wont as it's overwriting the app execution alias.

* ##### Confusing App Execution Alias Behaviour
  The usage of app execution aliases is confusing. If you use the online
  installer and for get to tick the box to to add to path, when you try and use
  `python`, you either get no output or the Microsoft Store opens. This hides the
  command not found error which would have indicated that their install didn't
  work as expected.
