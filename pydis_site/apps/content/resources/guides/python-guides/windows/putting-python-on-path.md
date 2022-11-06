---
title: Putting Python on Path
description: How to make sure Python is properly on the Windows Path environment variable
---

If you're on Windows and know you have [Python installed from python.org](https://www.python.org/downloads/) ([our
recommended way](../installing-python.md)) but you're still getting errors like

```text
pip : The term 'pip' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

when trying to run a [pip](https://pip.pypa.io/en/stable/) or [pyinstaller](https://pypi.org/project/pyinstaller/)
command, or running `python` [unexpectedly opens up the Microsoft
Store](../microsoft-store.mdconfusing-app-execution-alias-behaviour), the issue is likely that your Windows Path
environment variable is improperly configured for Python. This just means Windows doesn't know how to find your Python
installation.

The Path (or PATH) environment variable is what Windows uses to locate executables needed on the command line. Whenever
you type a command name in your terminal, like `python` or `pip`, the terminal looks for an exe with the same name in
the folders listed in the Path, so the command can be run.

The [Python installer](https://www.python.org/downloads/) provides an option to add Python to your Path automatically,
although it is not checked by default so many people miss it:

![Add Python to path installer checkbox.](/static/images/content/python-on-windows/installer_path_checkbox.png)

But don't worry, you can have the installer add it after the fact, or add it yourself! Continue on just below to the
[safe method](#safe-method-let-the-installer-add-python-to-path) to have the installer put Python on Path for you, or,
if you want to learn a handy Windows programming skill, skip to the [advanced
method](#advanced-method-manually-edit-the-path) that explains how to edit the Path manually.

## Safe method: Let the installer add Python to Path

The easiest and safest way to add Python to Path is by rerunning the installer. For this you will need the same
installer you used to install Python, which you can download again if needed from
[python.org](https://www.python.org/downloads/windows/), or it may still be in your Downloads folder (it's a file like `python-3.11.0-amd64.exe`).

Once you have it, here are the steps to modify the installation to add Python to Path:

1. Run the installer by double clicking it.

    ![Step 1](/static/images/content/python-on-windows/safe_path_method_1.png)

2. Select "Modify". (If you don't see the "Modify/Repair/Uninstall" screen then you likely have the wrong installer.)

    ![Step 2](/static/images/content/python-on-windows/safe_path_method_2.png)

3. Hit "Next" to move past the "Optional Features" screen.

    ![Step 3](/static/images/content/python-on-windows/safe_path_method_3.png)

4. Check "Add Python to environment variables" on the "Advanced Options" screen.

    ![Step 4](/static/images/content/python-on-windows/safe_path_method_4.png)

5. Hit install!

    ![Step 5](/static/images/content/python-on-windows/safe_path_method_5.png)

Then, after a moment, it should say "Modify was successful" and you can close the installer, and Python should now be on your Path! **You will need to restart any terminals or editors you have open before they detect the change.**

(These steps are for the Python 3.11 installer may differ slightly for other versions. Also, for step 1, if preferred, you can find your Python installation in the "Apps & features" Windows settings and hit "Modify" there, but you will still need to locate the installer exe at step 5 if it's not already in Downloads.)

To check that it worked, open a terminal &mdash; Command Prompt, Powershell, an IDE-integrated terminal, [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701), whichever you prefer, just _not_ the Python terminal with the `>>>` prompt &mdash; and run

```text
python -V
```

and then

```text
pip -V
```

and you should see the versions of Python and pip that you just added to Path:

![Checking Python and pip versions.](/static/images/content/python-on-windows/testing_path_worked_1.png)

You can also run Python with `python`, and then after `>>>` in the Python REPL, run

```py
import sys; print(sys.executable)
```

to see that the exact executable that is currently running Python is what you expect:

![Checking Python executable.](/static/images/content/python-on-windows/testing_path_worked_2.png)

(Type `exit()` from here to go back to the normal terminal.)

<!-- TODO mention that py may open a different version and link to py launcher guide. -->

Of course your username will probably not be "r" like mine is, and your executable path may differ from
`C:\Users\<user>\AppData\Local\Programs\Python\Python311` depending on where you chose to install Python and what
version you have. The last folder will be `Python310` for Python 3.10, `Python39` for Python 3.9, etc. But those
differences don't matter if `python` and `pip` and other things like `pyinstaller` (if you've pip installed it) now work
for you!

Hopefully things are indeed working, _however_, it is possible that, due to having multiple Python versions, or other mixups,
the commands are still not behaving how you expect. If so, read on to learn how to manually edit the Path environment variable. It's really not that hard and a super useful Windows skill to know for more than just Python.

## Advanced Method: Manually edit the Path

TODO!!!
