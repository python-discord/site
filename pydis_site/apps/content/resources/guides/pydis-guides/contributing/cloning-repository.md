---
title: Cloning a Repository
description: A guide to cloning git repositories.
icon: fab fa-github
---

> **Note:** The process varies depending on your choice of code editor / IDE, so refer to one of the following guides:

- [Cloning with PyCharm](#cloning-with-pycharm)
- [Cloning with the command line](#cloning-with-the-command-line)

The following will use the [Sir-Lancebot](https://github.com/python-discord/sir-lancebot/) repository as an example, but the steps are the same for all other repositories. You should have already retrieved your fork's Git URL as described in [**Creating a Fork**](../forking-repository).

---

## Cloning with the command line

1. Clone your forked repository using `git clone` followed by your fork's Git URL. Then, change your working directory to the repository.

```shell
$ git clone https://github.com/<your username>/sir-lancebot
...
$ cd sir-lancebot
```

---

## Cloning with PyCharm

1. Load up PyCharm and click `Get from VCS`.<br>
   ![Create Project in PyCharm](/static/images/content/contributing/pycharm_create_project.png)
2. Enter the URL of your forked repository.
3. Change the directory if you desire and click `Clone`.<br>
   ![Clone Git Project in Pycharm](/static/images/content/contributing/pycharm_checkout.png)
