---
title: Working with the Git CLI
description: Basic workflow when using the git CLI.
toc: 2
---

This is the basic workflow when working with Git with CLI. For the PyCharm version of the guide, [**click here**](../pycharm).
The following will use the [Sir-Lancebot](https://github.com/python-discord/sir-lancebot/) repository as an example, but the steps are the same for all other repositories.

> **Note:** This is a guide only meant to get you started with git. For in-depth resources, check the [**Working with Git**](..) page.

---

## Adding the Upstream Remote
Adding a *remote* to the main GitHub repository you forked off will allow you to later update your fork with changes from the main repository.

Generally, a *remote* designates a repository that is on GitHub or another external location rather than on your computer.
The `origin` remote will refer to your fork on GitHub. The `upstream` remote will refer to the main repository on GitHub.
```sh
$ git remote add upstream https://github.com/python-discord/sir-lancebot.git
```
If you use SSH, use `git@github.com:python-discord/sir-lancebot.git` for the upstream URL instead.

---

## Creating a New Branch
You will be committing your changes to a new branch rather than to `main`.
Using branches allows you to work on muiltiple pull requests without conflicts.

You can name your branch whatever you want, but it's recommended to name it something succinct and relevant to the changes you will be making.

Run the following commands to create a new branch. Replace `branch_name` with the name you wish to give your branch.
```sh
$ git fetch --all
...
$ git checkout --no-track -b branch_name upstream/main
```

---

## Staging Changes
Files in git can be in one of four different states:

- *Staged*: These files have been modified and will be committed.
- *Unstaged*: These files were already present but have been modified.
- *Untracked*: These files are new to the repository.
- *Ignored*: Specified in a `.gitignore` file in the project root, these files will never be committed, remaining only on your computer.

As you can see, only staged files will end up being committed.
You can get an overview of this using `git status`.
If you wish to commit unstaged or untracked files, you will need to add them with `git add` first.
```sh
# Add files individually
$ git add path/to/file.py path/to/other/file.py

# Add all unstaged and untracked files in a directory
$ git add path/to/directory

# Add all unstaged and untracked files in the project
$ git add .

# Add all tracked and modified files in the project
$ git add -u

# Unstage a file
$ git reset -- path/to/file.py
```

---

## Discarding Changes
Be careful, these operations are **irreversible**!
```sh
# Discard changes to an unstaged file
$ git checkout -- path/to/file.py

# Discard ALL uncommitted changes
$ git reset --hard HEAD
```

---

## Committing Changes
The basic command for committing staged changes is `git commit`. All commits must have a message attached to them.
```sh
# Commit staged changes and open your default editor to write the commit message
$ git commit

# Specify the message directly
$ git commit -m "Turn pride avatar into an embed"

# Commit all staged and unstaged changes. This will NOT commit untracked files
$ git commit -a -m "Update d.py documentation link"
```

---

## Pushing Commits
Commits remain local (ie. only on your computer) until they are pushed to the remote repository (ie. GitHub).

The first time you push on your new branch, you'll need to set the upstream when you push:
```sh
$ git push -u origin branch_name
```
Any subsequent pushes can be done with just `git push`.

---

## Pulling Changes
Sometimes you want to update your repository with changes from GitHub.
This could be the case if you were working on the pull request on two different computers and one of them has an outdated local repository.

You can pull the changes from GitHub with:
```sh
$ git pull
```
You can also pull changes from other branches such as from branch `main` in `upstream`:
```sh
$ git pull upstream main
```
This should generally only be needed if there are [merge conflicts](https://help.github.com/en/articles/about-merge-conflicts) that you need to resolve manually. Conflicts arise when you change the same code that someone else has changed and pushed since you last updated your local repository.
