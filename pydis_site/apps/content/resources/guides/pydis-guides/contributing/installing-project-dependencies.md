---
title: Installing Project Dependencies
description: A guide to installing the dependencies of our projects.
icon: fab fa-python
---

> **Note:** The process varies depending on your choice of code editor / IDE, so refer to one of the following guides:

- [Installing dependencies with the command line](#installing-dependencies-with-the-command-line)
- [Installing dependencies with PyCharm](#installing-dependencies-with-pycharm)

The following will use the [Sir-Lancebot](https://github.com/python-discord/sir-lancebot/) repository as an example, but the steps are the same for all other repositories.
You should have already cloned your fork as described in [**Cloning a Repository**](../cloning-repository).

---

## Installing dependencies with the command line

1. Make sure you are in the root project directory. This directory will always have a file titled `README.md`.
2. Install project and development dependencies. Remember to also set up pre-commit hooks to ensure your pushed commits will never fail linting.

---

```shell
$ uv sync
$ uv run task precommit
```

---
