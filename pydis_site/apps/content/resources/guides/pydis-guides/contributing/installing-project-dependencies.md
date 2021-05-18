---
title: Installing Project Dependencies
description: A guide to installing the dependencies of our projects.
icon: fab fa-python
---

> **Note:** The process varies depending on your choice of code editor / IDE, so refer to one of the following guides:

- [Installing dependencies with PyCharm](#installing-dependencies-with-pycharm)
- [Installing dependencies with the command line](#installing-dependencies-with-the-command-line)

The following will use the [Sir-Lancebot](https://github.com/python-discord/sir-lancebot/) repository as an example, but the steps are the same for all other repositories.
You should have already cloned your fork as described in [**Cloning a Repository**](../cloning-repository).

---

## Installing dependencies with PyCharm
1. Load up your project in PyCharm.
2. Go to the Project Settings by clicking `File`, then `Settings...`. Alternatively, use the shortcut key: `Ctrl+Alt+S` (`command+comma` on Mac OS).
3. Install the [poetry plugin](https://plugins.jetbrains.com/plugin/14307-poetry).
4. Navigate to `Project Interpreter`, then click the gear icon and click `Add`.<br/>
![PyCharm Interpreter Settings](/static/images/content/contributing/pycharm_interpreter.png)<br/>
5. Click `Poetry Environment`, then click `OK`.<br/>
![PyCharm Pipenv Environment](/static/images/content/contributing/pycharm_poetry.png)<br/>
6. PyCharm will automatically install the packages required into a virtual environment.<br/>
![PyCharm Project Interpreter](/static/images/content/contributing/pycharm_poetry_success.png)

---

## Installing dependencies with the command line
1. Make sure you are in the root project directory. This directory will always have a file titled `README.md`.
2. Install project and development dependencies. Remember to also set up pre-commit hooks to ensure your pushed commits will never fail linting.
---


```shell
$ poetry install
$ poetry run task precommit
```
