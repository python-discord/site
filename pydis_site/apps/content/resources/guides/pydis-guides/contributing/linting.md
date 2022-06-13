---
title: Linting
description: A guide for linting and setting up pre-commit.
---

Your commit will be rejected by the build server if it fails to lint.
On most of our projects, we use `flake8` and `pre-commit` to ensure that the code style is consistent across the code base.

`pre-commit` is a powerful tool that helps you automatically lint before you commit.
If the linter complains, the commit is aborted so that you can fix the linting errors before committing again.
That way, you never commit the problematic code in the first place!

Please refer to the project-specific documentation to see how to setup and run those tools.
In most cases, you can install pre-commit using `poetry run task precommit`, and lint using `poetry run task lint` in the console.
