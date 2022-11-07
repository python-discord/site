---
title: Installing Python on Windows
description: How we recommend installing Python on Windows
icon: fab fa-windows
---

Our recommended way of installing Python on Windows is using a full installer from the official [python.org Downloads
page](https://www.python.org/downloads/). Installing Python from the [Microsoft
Store](https://apps.microsoft.com/store/search/python) is _not_ recommended as [it can cause various
issues](../microsoft-store).

On [python.org/downloads](https://python.org/downloads), click the big yellow "Download Python 3.x.x" button near the top of the page and it should automatically start a download of the installer for the latest stable version of Python
that best suits your computer.

## Selecting an Installer

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

## Running the installer

When you run the installer you should see a screen like this:

![python_installer_screen](https://user-images.githubusercontent.com/22353562/126144479-cfe6bd98-6d2e-47c3-b6b3-5de9f2656e9a.png)

Make sure you tick "Add Python 3.x to Path". This allows you to use the `python`
and `pip` commands in your terminal to invoke Python. If you already have a
Python installation on your PATH and don't want this one to override it, don't
tick this.

If you installed Python without adding to PATH and now want to add it, see
[our guide on adding Python to PATH](../putting-python-on-path).

Then simply click install, and wait for the install to finish!

To test your installation, type "cmd" in the windows search bar and select
"Command Prompt" to open a terminal (make sure it's opened _after_ installation
has finished) type `python -V`, and press enter. If it outputs your python
version, you've successfully installed Python. (if you didn't add to PATH, you
can use [the py launcher](../py-launcher) to test
instead).
