---
title: Adding Python to the Path
description: How to make sure Python is properly on the Windows Path environment variable
icon: fab fa-windows
toc: 2
---

If you're on Windows and know you have [Python installed from python.org](https://www.python.org/downloads/) ([our
recommended way](../installing-and-using-python)) but you're still getting errors like

```text
pip : The term 'pip' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

when trying to run a [`pip`](https://pip.pypa.io/en/stable/) or [`pyinstaller`](https://pypi.org/project/pyinstaller/)
command, or running `python` [unexpectedly opens up the Microsoft
Store](../microsoft-store#confusing-app-execution-alias-behaviour), the issue is likely that your Windows Path
environment variable is improperly configured for Python. This just means Windows doesn't know how to find your Python
installation.

The Path (or PATH) environment variable is what Windows uses to locate executables needed on the command line. Whenever
you type a command name in your terminal, like `python` or `pip`, the terminal looks for a program of the same name in
the folders listed in the Path, so the command can be run.

The [python.org Python installer](https://www.python.org/downloads/) provides an option to add Python to your Path
automatically, although it is not checked by default so many people miss it:

[![Add Python to path installer checkbox.](/static/images/content/python-on-windows/installer_path_checkbox.png)](/static/images/content/python-on-windows/installer_path_checkbox.png)

But don't worry, you can have the installer add it after the fact, or add it yourself! Continue on just below to the
[safe method](#safe-method-let-the-installer-add-python-to-path) to have the installer put Python on Path for you. Or,
if you want to learn a handy Windows programming skill, skip to the [advanced
method](#advanced-method-manually-edit-the-path) that explains how to edit the Path manually.

## Safe method: Let the installer add Python to Path

The easiest and safest way to add Python to Path is by rerunning the installer. For this you will need the same
installer you used to install Python, which you can download again if needed from
[python.org](https://www.python.org/downloads/windows/), or it may still be in your Downloads folder (it's a file named
something like `python-3.11.0-amd64.exe`).

Once you have it, here are the steps to modify the installation to add Python to Path:

1. Run the installer by double clicking it.

    [![Step 1](/static/images/content/python-on-windows/safe_path_method_1.png)](/static/images/content/python-on-windows/safe_path_method_1.png)

2. Select "Modify". (If you don't see the "Modify/Repair/Uninstall" screen then you likely have the wrong installer.)

    [![Step 2](/static/images/content/python-on-windows/safe_path_method_2.png)](/static/images/content/python-on-windows/safe_path_method_2.png)

3. Hit "Next" to move past the "Optional Features" screen.

    [![Step 3](/static/images/content/python-on-windows/safe_path_method_3.png)](/static/images/content/python-on-windows/safe_path_method_3.png)

4. Check the "Add Python to environment variables" checkbox on the "Advanced Options" screen.

    [![Step 4](/static/images/content/python-on-windows/safe_path_method_4.png)](/static/images/content/python-on-windows/safe_path_method_4.png)

5. Hit install!

    [![Step 5](/static/images/content/python-on-windows/safe_path_method_5.png)](/static/images/content/python-on-windows/safe_path_method_5.png)

Then, after a moment, it should say "Modify was successful" and you can close the installer. Python should now be on
your Path! **You will need to restart any terminals or editors you have open before they detect the change.**

(These steps are for the Python 3.11 and installer may differ slightly for other versions. Also, for step 1, if
preferred, you can find your Python installation in the "Apps & features" Windows settings and hit "Modify" there, but
will still need to locate the installer exe at step 5 if it's not already in Downloads.)

### Verifying your changes

To check that it worked, open a fresh terminal &mdash; Command Prompt, PowerShell, an IDE-integrated terminal, [Windows
Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701), whichever you prefer, just _not_ the
Python terminal with the `>>>` prompt &mdash; and run

```text
python -V
```

and then

```text
pip -V
```

and you should see the versions of Python and pip that you just added to Path:

[![Checking Python and pip versions.](/static/images/content/python-on-windows/testing_path_worked_1.png)](/static/images/content/python-on-windows/testing_path_worked_1.png)

Running `Get-Command python` in PowerShell, or `where python` in Command Prompt, you
can see where that terminal is finding the `python.exe` it would run when a `python` command is given:

[![Get-Command/where Python.](/static/images/content/python-on-windows/testing_path_worked_2.png)](/static/images/content/python-on-windows/testing_path_worked_2.png)

(`where` in fact lists all the Pythons it finds, even the dummy [app execution
alias](../microsoft-store#confusing-app-execution-alias-behaviour) one that opens the Microsoft Store.)

You can also run Python with `python` (not `py` as that may start a different version, see more
[here](../installing-and-using-python/#the-py-launcher)), and then after `>>>` in the Python REPL, run

```py
import sys; print(sys.executable); exit();
```

to see that the exact executable that is currently running Python is what you expect:

[![Checking Python executable.](/static/images/content/python-on-windows/testing_path_worked_3.png)](/static/images/content/python-on-windows/testing_path_worked_3.png)

Of course your username will probably not be "r", and your executable path may differ from
`C:\Users\<user>\AppData\Local\Programs\Python\Python311` depending on where you chose to install Python and what
version you have. The last folder will normally be `Python310` for Python 3.10, `Python39` for Python 3.9, etc. But
those differences don't matter if `python` and `pip` and other things like `pyinstaller` (if you've [pip
installed](https://pypi.org/project/pyinstaller/) it) now work for you!

Hopefully things are indeed working, however, it is possible that, due to having multiple Python versions, or other
mixups, the commands are still not behaving how you expect. If so, read on to learn how to manually edit the Path. (If
you already did that, open a help channel on the [Python Discord server](https://discord.com/invite/python) explaining
everything you've tried so far, and someone will hopefully be able to help.)

## Advanced Method: Manually edit the Path

### About the Path

As mentioned above, the Path (often called "PATH", though it shows up as "Path") is what Windows uses to locate
executables needed on the command line. If it's misconfigured, `python` and `pip` commands may not work as
expected.

"Path" is the name of a Windows environment variable whose value is simply a list of paths to folders on the system. A
_path_ is just string that locates a folder, like `C:\Program Files\Git\cmd`. An _environment variable_ is a variable (a
thing with a name and a value) that is available to the entire system, or at least to an entire user of the system.

In fact, the Windows Path is technically _two_ environment variables, two lists of folders: a System one and a User one.
But, as explained [here](https://superuser.com/a/878382), when actually used, the User Path is appended to the System
Path, forming one long list.

So, how it works is whenever you type a command like `python` into a terminal, the terminal looks for a matching
runnable file like `python.exe` ([or `python.bat`](https://en.wikipedia.org/wiki/Batch_file)) in each of the folders
listed in the Path, starting with the System Path (top to bottom), and then the User Path (top to bottom). It stops
searching on the first one it finds and runs that program with the command line arguments you may have given it, hence
(hopefully) running Python from an installed `python.exe`.

If it can't find a runnable file that matches the command name, it spits out an error like:

```text
foobar: The term 'foobar' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

Or, in the case of not finding `python`, it may [open up the Microsoft
store](../microsoft-store#confusing-app-execution-alias-behaviour).

Again, the Path lookup order is:

> System Path (top to bottom) &rarr; User Path (top to bottom) &rarr; Command not found error

### Adding Python to your Path

Here only the common case of adding Python and the Python Scripts directory to the Windows Path is detailed. However,
knowing how to manually modify the Path is handy beyond just Python for whenever you need to change or debug which
programs run on the command line in Windows. (The less customizable but [safer method is
above](#safe-method-let-the-installer-add-python-to-path) if you missed it.)

Follow these steps to add Python to the Path. **You will need administrator privileges on your computer.**

1.  First, find the folder path your Python executable is in. There are a few ways to do this:

    **Way 1**: Run `py -0p` on the command line and copy the folder path of the version you want:

    [![Finding exe with py.](/static/images/content/python-on-windows/finding_exe_1.png)](/static/images/content/python-on-windows/finding_exe_1.png)

    **Way 2**: Run `import sys; print(sys.executable)` in Python on your PC and copy the folder path it prints out:

    [![Finding exe in repl.](/static/images/content/python-on-windows/finding_exe_2.png)](/static/images/content/python-on-windows/finding_exe_2.png)

    **Way 3**: Root around a bit in your `C:\Users\<user>\AppData\Local\Programs\Python` folder or wherever you
    installed Python to find the path to the folder that has the `python.exe` in it.

    I end up with `C:\Users\r\AppData\Local\Programs\Python\Python311\` (no `python.exe` at the end).
    Your path will of course be based on your username (my username is "r") and your version of Python, such as
    `C:\Users\ducky\AppData\Local\Programs\Python\Python39\` if your username is "ducky" and you're using Python 3.9.
    Copy your path. We'll use it in steps 6 and 7.

2.  [**This step is optional but helpful to see what's going on.**] Copy the folder path from step 1 into the path bar
    of Windows File Explorer. In the folder you should be able to see `python.exe`, and in the Scripts subfolder, things
    like `pip.exe` and `pyinstaller.exe` (if you have it installed).

    [![Finding exes in folder.](/static/images/content/python-on-windows/finding_exe_3.png)](/static/images/content/python-on-windows/finding_exe_3.png)

    These are the executables we want the command line to be able to find via the Windows Path.

3.  Now, type "environment variables" in the Start menu or Start search box and open the "Edit the system environment
    variables" option.

    [![Step 3](/static/images/content/python-on-windows/edit_path_1.png)](/static/images/content/python-on-windows/edit_path_1.png)

4.  Hit the "Environment Variables..." button.

    [![Step 4](/static/images/content/python-on-windows/edit_path_2.png)](/static/images/content/python-on-windows/edit_path_2.png)

5.  Then in a new window you should see two "Path" variables, one under "User variables for &lt;user&gt;" and one under
    "System variables". Select one of them (most likely the User Path) and hit the "Edit..." button underneath it.

    [![Step 5](/static/images/content/python-on-windows/edit_path_3.png)](/static/images/content/python-on-windows/edit_path_3.png)

    You should use the User Path (what the screenshots show) for the default installation of Python. In general, only
    put things on the System Path if they are installed for all users (e.g. in `C:\Program Files` or `C:\`) and you're
    certain they won't overshadow anything in User Paths. **Remember, the System Path takes precedence over the User
    Path when commands are looked up.**

    (Don't worry if your variables or Path contents differ a bit from those shown.)

6.  Now a third window opens and this is where the Path is actually edited. It shows the ordered list of the folders on
    the Path and you can select the entries, edit them, reorder them, make new ones, delete them and so on. (Don't
    delete any unless you know what you're doing!)

    We want to add the Python executable path we found in step 1 as a new entry, so click "New" and paste in the path.

    [![Step 6](/static/images/content/python-on-windows/edit_path_4.png)](/static/images/content/python-on-windows/edit_path_4.png)

7.  We also need to add the Python Scripts directory to the Path to have commands like `pip` and `pyinstaller` work. So
    hit "New" and paste in the Python executable path again, and type "Scripts" after it.

    [![Step 7](/static/images/content/python-on-windows/edit_path_5.png)](/static/images/content/python-on-windows/edit_path_5.png)

    (It doesn't matter whether or not they have trailing backslashes.)

8.  Finally, select each of the paths you just added in turn and move them to the very top of the list using the "Move
    Up" button. (Their relative order should not matter.)

    [![Step 8](/static/images/content/python-on-windows/edit_path_6.png)](/static/images/content/python-on-windows/edit_path_6.png)

    This step may not be strictly necessary, but remember that command lookup happens in order from top to bottom.
    Python is often bundled with other software that may end up on the Path, so there could be another
    `python.exe` in one of of the other folders on the path that gets in the way. (This exact thing has happened to me
    when I put `C:\Program Files\Inkscape\bin` on my Path, as [Inkscape](https://inkscape.org/) comes with a copy of
    Python.)

    > _8.5._ Recall, the System Path comes before the User Path during command lookup, so to be certain you to may want
    > to go back and check the "System variables" Path (see step 5) and _carefully_ delete any entry that you're sure is
    > a path to a Python executable overshadowing the one you just added. Though please, don't delete any Path entries
    > you're aren't certain about! Just in case, for reference, [here are the important looking System Path
    > entries](/static/images/content/python-on-windows/system_path_important.png) on my 64-bit Windows 10 PC.

9.  Finish by making sure to hit "OK" on each of the thee "Edit environment variable", "Environment Variable", and
    "System Properties" windows, and then you're done! (If you accidentally hit Cancel the changes may not be saved.)

    Python and Python Scripts should now be on your Path! **You will need to restart any terminals or editors you have
    open before they detect the change.**

At this point you can [verify your changes in the same way as detailed above](#verifying-your-changes). Hopefully it
works!

(These steps were written with Windows 10 and Python 3.11 in mind, but they should be identical or similar for Windows
11 and other recent versions of Python.)
