---
title: Creating a Unix-style Python Environment on Windows
description: How to setup Python for Windows.
---

Many programmers use Linux or macOS operating systems for their work, though newcomers to programming will likely want to get started on the computer they already own, which will often be running Windows.
This guide will help you install Python on Windows.

Programmers also need to become comfortable using a command prompt (also known as a terminal), and many guides for both beginning and advanced programming will often tell you certain commands to run.
The Windows command prompt has different names for similar commands that are available on Linux and macOS.
This guide will also help you set up a command prompt called Git Bash, which will support many of the commands available on Linux and macOS.

## Installing Python
Python can be downloaded from the Python website on the [downloads page](https://www.python.org/downloads/).
The website will automatically present you with a download button for the latest release of the Windows version when you access the site from a Windows machine.

Once the download is complete, you can begin the installation.
Select "Customize Installation".
The default settings for "Optional Features" are sufficient and you can click "Next".

The next step is to decide on a location where the Python executable can be stored on your computer.
This should be a location that's easy for you to remember.
One possibility is to create a folder called "Python" at the root of your hard drive.
Once you have selected a location, you can click "Install", as no other settings on this screen need to be adjusted.
This will complete the installation.

## Installing a text editor
You will also need a text editor for writing Python programs, and for subsequent steps of this guide.
Powerful programs called integrated development environments (IDEs) like PyCharm and Visual Studio Code contain text editors, but they also contain many other features with uses that aren't immediately obvious to new programmers.

[Notepad++](https://notepad-plus-plus.org/) is a popular text editor for both beginners and advanced users who prefer a simpler interface.
Other editors we recommend can be found [here](https://pythondiscord.com/resources/tools/#editors).

## Installing Git Bash
Git is a command line program that helps you keep track of changes to your code, among other things.
Many developers use it, and while you may not need it right away, it is useful to install it because it comes with Git Bash.
On the "Select Components" screen, no settings need to be changed.
The next screen will ask what text editor you want to use with Git. Vim is the default choice, though Vim is widely considered difficult to learn, so you may choose to select Notepad++ or whichever text editor you may have installed previously.

For all remaining screens in the installation, the default selections are fine.

## Configuring .bashrc
`.bashrc` is a file where we tell Git Bash where the Python executable is.
First, open Git Bash, and as your first command, type `echo ~` and hit enter.
This will most likely print `c/Users/YourUsername` to the terminal.
Navigate to this location in your file explorer, though keep in mind that Windows will display `c/Users/YourUsername` as `C:\Users\YourUsername`.
In this folder, there will be a file called `.bashrc`; open it with your text editor of choice.

For this step, you will need to remember where you installed Python earlier.
In whichever folder that was, there is a file called `python.exe`; this is the executable that will run your Python programs.
Copy the full path of this file, starting from `C:`.
If you used the example location given earlier, it will be located at `C:\Python\python.exe`.

In the `.bashrc` file, add a line to the end of the file saying `alias python='C:\\Python\\python.exe`, where `C:\\Python\\python.exe` is the location of your `python.exe` file, but each folder is separated by two backslashes instead of one.
The two backslashes are because a single backslash is used as an [escape character](https://en.wikipedia.org/wiki/Escape_character).
Save the file, and then type `source ~/.bashrc` to activate the change you have made.

Finally, enter `python -c 'import sys; print(sys.executable)'` into Git Bash.
(If you attempt to copy and paste this into the terminal using Ctrl+V, it might not work, though Shift+Insert will.)
If all the steps have been followed correctly, this will print the location of your `python.exe` file and demonstrate that your environment is set up correctly.
You can hereafter use the `python` command in Git Bash to run any Python program that you write.

## Running a test program
At any location on your computer, create a file named `hello.py` and open it with your text editor.
The program need only be one line: `print('Hello world!')`.
Save this file.

To run this program in Git Bash, navigate to where it is saved on your hard drive.
If you know the path to this location, you can use the `cd` command ("cd" stands for "change directory") to navigate to it.
If it's saved to your desktop, `cd /c/Users/YourUsername/Desktop` will take you there.
Otherwise if you have the directory open in your file explorer, you can right click anywhere in the white space of the file explorer window (not on top of a file) and select "Git Bash Here".
Once you're there, type `python hello.py`, and the program will run.
