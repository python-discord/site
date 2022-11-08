---
title: Installing and Using Python on Windows
description: How we recommend installing Python on Windows, and how to use Python Windows features
icon: fab fa-windows
toc: 2
---

Our recommended way of installing Python on a Windows operating system is using the full installer from the official
[python.org Downloads page](https://www.python.org/downloads/) (the main yellow button) using the default options, except
making sure to check the "Add python.exe to PATH" checkbox. Getting Python from the [Microsoft
Store](https://apps.microsoft.com/store/search/python) is _not_ recommended as [it can cause various
issues](../microsoft-store).

This guide gives detailed instructions on that [recommended way to install Python on Windows](#recommended-install),
then goes on to discuss [more information about installing Python on Windows](#more-installation-information), and
finally wraps up by explaining some common Windows-specific Python usage, namely the [py launcher](#the-py-launcher),
and how to work with [virtual environments](#virtual-environments).

You may also want to check out our guides on [Common Issues Using Python on Windows](../common-issues), [Adding Python
to the Windows Path](../putting-python-on-path.md), and Setting up a [Unix-Style Environment on
Windows](../unix-env-on-windows.md).

## Recommended Install

Follow the steps below to install the latest version of Python on Windows.

(The instructions were written with Windows 10 and Python 3.11.0 in mind, but should be nearly or fully identical on
Windows 11 and other modern versions of Python.)

> If you want a fresh start, you may want to first uninstall any other versions of Python on your PC, including those from
> the Microsoft Store, if you have any. This can be done in the ["Apps & features" Windows
> settings](/static/images/content/python-on-windows/ms_store_uninstall.png) (type "apps and features" into the Start Menu
> to find it). Though it's fine to have multiple versions of Python installed at once. It can be useful for testing
> version compatibility or for working on projects made in a certain version. Only uninstall things if you want to.

1.  Go to [python.org/downloads](https://www.python.org/downloads) and click the big yellow "Download Python 3.x.x"
    button near the top of the page. That should start the download of the latest Windows Python installer that best
    suits your computer.

    If you want a different version or it doesn't work for some reason, you can download the
    Windows installer you want from [python.org/downloads/windows](https://www.python.org/downloads/windows).

    [![Step 1](/static/images/content/python-on-windows/recommended_install_1.png)](/static/images/content/python-on-windows/recommended_install_1.png)

2.  When it finishes downloading, click the file in your browser or find it in your Downloads folder and double-click it to start the installer.

    [![Step 2](/static/images/content/python-on-windows/recommended_install_2.png)](/static/images/content/python-on-windows/recommended_install_2.png)

3.  Check the "Add python.exe to PATH" checkbox (the text may differ slightly depending on your installer). This will
    make it so the command line can recognize commands like `python` and `pip`. (Read [this
    guide](../putting-python-on-path) to learn more.)

    [![Step 3](/static/images/content/python-on-windows/recommended_install_3.png)](/static/images/content/python-on-windows/recommended_install_3.png)

4.  Then click the big "Install Now" button. Aside from adding Python to PATH, the rest of the installer defaults are
    usually fine, so there's no need to customize the installation unless you want to.

    [![Step 4](/static/images/content/python-on-windows/recommended_install_4.png)](/static/images/content/python-on-windows/recommended_install_4.png)

5.  It will take a minute to install and then (hopefully) say "Setup was successful". Congrats, you just installed
    Python! You can close the installer.

    [![Step 5 A](/static/images/content/python-on-windows/recommended_install_5.png)](/static/images/content/python-on-windows/recommended_install_5.png)
    [![Step 5 B](/static/images/content/python-on-windows/recommended_install_6.png)](/static/images/content/python-on-windows/recommended_install_6.png)

### Checking that it Worked

To test that installing Python worked, you can do what it suggests and search "python" on the Start Menu to find the Python console app
and run some code like `print("Hello, World!")`.

[![Testing Python console](/static/images/content/python-on-windows/recommended_install_7.png)](/static/images/content/python-on-windows/recommended_install_7.png)

Or try the more usual way of running Python by typing `py` or `python` in a new terminal window to open up the Python
[REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop), or use `python somefile.py` to run some
Python file (if `py` runs the wrong version of Python, [see below](#the-py-launcher) for how to change the default). Use
whichever terminal you prefer: Command Prompt, PowerShell, an IDE-integrated terminal, [Windows
Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701). It just has to be a freshly opened
terminal or the commands may not be recognized.

[![Testing py and python](/static/images/content/python-on-windows/recommended_install_8.png)](/static/images/content/python-on-windows/recommended_install_8.png)

You can double check what versions of Python and [pip](https://pip.pypa.io/en/stable/) were installed by running `python -V` or `pip -V` in a terminal:

[![Checking python and pip versions](/static/images/content/python-on-windows/testing_path_worked_1.png)](/static/images/content/python-on-windows/testing_path_worked_1.png)

And finally, it's worth searching and opening "IDLE" on the Start Menu, which is the the basic
[IDE](https://en.wikipedia.org/wiki/Integrated_development_environment) that comes with Python. Most people end up using
[PyCharm](https://www.jetbrains.com/pycharm/) or [VSCode](https://code.visualstudio.com/) to program in Python but IDLE
is a great starting point.

[![Testing IDLE](/static/images/content/python-on-windows/recommended_install_9.png)](/static/images/content/python-on-windows/recommended_install_9.png)

## More Installation Information

### Selecting an Installer

There are many different installer options available from the downloads page.
You should usually select the "Windows installer" option instead of the "Windows
embeddable package". Some minor versions may not

### Which version?

Current Python versions follow the form `3.minor.micro`. Major releases happen
yearly and provide new features and breaking changes, whilst minor releases are
more common and only include bug/security fixes.

Installing the latest major version will give you access to Python's newest
features. However, some modules may not support the newest versions straight
away, so installing the second latest will help you avoid those issues. If you
find you want some newer features or your module does not support your current
version, you can always install another version as well.

You should generally always install the newest minor version, although some may
not provide an installer in which case you should find the newest that does.

### 32-bit vs 64-bit?

Install 64-bit python unless you have reason not to. With 32 bit you may run
into memory limits if doing intensive operations (Python will be limited to
using 4GB of memory), and some installed modules may not offer prebuilt wheels
for 32 bit, potentially making installs slower or meaning you have to install
build dependencies.

If you get an error when installing 64-bit Python, your computer may not support
it. To find out if this is the case, search "About your PC" in windows search
and open the settings page. Then look for the "System Type" option under "Device
Specifications". It should say "64-bit operating system, x64-based processor" if
you have support. You need a 64 bit processor and OS to install 64 bit programs.

### Running the installer

When you run the installer you should see a screen like this:

![python_installer_screen](https://user-images.githubusercontent.com/22353562/126144479-cfe6bd98-6d2e-47c3-b6b3-5de9f2656e9a.png)

Make sure you tick "Add Python 3.x to Path". This allows you to use the `python`
and `pip` commands in your terminal to invoke Python. If you already have a
Python installation on your PATH and don't want this one to override it, don't
tick this.

If you installed Python without adding to PATH and now want to add it, see
[our guide on adding Python to PATH](../putting-python-on-path).

Then simply click install, and wait for the install to finish!

To test your installation, type "cmd" in the windows search bar and select "Command Prompt" to open a terminal (make
sure it's opened _after_ installation has finished) type `python -V`, and press enter. If it outputs your python
version, you've successfully installed Python. (if you didn't add to PATH, you can use [the py
launcher](../installing-and-using-python/#the-py-launcher) to test instead).

## The py Launcher

dg:TODO

## Virtual Environments

dg:TODO
