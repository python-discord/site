---
title: Supplemental Information
description: Additional information related to our contributing guidelines.
---

This page contains additional information concerning a specific part of our development pipeline.

## Writing Good Commit Messages

A well-structured git log is key to a project's maintainability; it provides insight into when and *why* things were done for future maintainers of the project.

Commits should be as narrow in scope as possible.
Commits that span hundreds of lines across multiple unrelated functions and/or files are very hard for maintainers to follow.
After about a week they'll probably be hard for you to follow, too.

Please also avoid making minor commits for fixing typos or linting errors.
*[Don’t forget to lint before you push!](https://soundcloud.com/lemonsaurusrex/lint-before-you-push)*

A more in-depth guide to writing great commit messages can be found in Chris Beam's *[How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/).*

## Code Style

All of our projects have a certain project-wide style that contributions should attempt to maintain consistency with.
During PR review, it's not unusual for style adjustments to be requested.

[This page](../../style-guide/) will reference the differences between our projects and what is recommended by [PEP 8.](https://www.python.org/dev/peps/pep-0008/)

## Linting and Pre-commit

On most of our projects, we use `flake8` and `pre-commit` to ensure that the code style is consistent across the code base.

Running `flake8` will warn you about any potential style errors in your contribution.
You must always check it **before pushing**.
Your commit will be rejected by the build server if it fails to lint.

**Some style rules are not enforced by flake8. Make sure to read the [style guide](../../style-guide/).**

`pre-commit` is a powerful tool that helps you automatically lint before you commit.
If the linter complains, the commit is aborted so that you can fix the linting errors before committing again.
That way, you never commit the problematic code in the first place!

Please refer to the project-specific documentation to see how to setup and run those tools.
In most cases, you can install pre-commut using `pipenv run precommit` or `poetry run task precommit`, and lint using `pipenv run lint` or `poetry run task lint`.

## Type Hinting

[PEP 484](https://www.python.org/dev/peps/pep-0484/) formally specifies type hints for Python functions, added to the Python Standard Library in version 3.5.
Type hints are recognized by most modern code editing tools and provide useful insight into both the input and output types of a function, preventing the user from having to go through the codebase to determine these types.

For example:

```python
import typing

def foo(input_1: int, input_2: typing.Dict[str, str]) -> bool:
    ...
```

This tells us that `foo` accepts an `int` and a `dict`, with `str` keys and values, and returns a `bool`.

If the project is running Python 3.9 or above, you can use `dict` instead of `typing.Dict`.
See [PEP 585](https://www.python.org/dev/peps/pep-0585/) for more information.

All function declarations should be type hinted in code contributed to the PyDis organization.

## Logging

Instead of using `print` statements for logging, we use the built-in [`logging`](https://docs.python.org/3/library/logging.html) module.
Here is an example usage:

```python
import logging

log = logging.getLogger(__name__) # Get a logger bound to the module name.
# This line is usually placed under the import statements at the top of the file.

log.trace("This is a trace log.")
log.warning("BEEP! This is a warning.")
log.critical("It is about to go down!")
```

Print statements should be avoided when possible.
Our projects currently defines logging levels as follows, from lowest to highest severity:

- **TRACE:** These events should be used to provide a *verbose* trace of every step of a complex process. This is essentially the `logging` equivalent of sprinkling `print` statements throughout the code.
- **Note:** This is a PyDis-implemented logging level. It may not be available on every project.
- **DEBUG:** These events should add context to what's happening in a development setup to make it easier to follow what's going while workig on a project. This is in the same vein as **TRACE** logging but at a much lower level of verbosity.
- **INFO:** These events are normal and don't need direct attention but are worth keeping track of in production, like checking which cogs were loaded during a start-up.
- **WARNING:** These events are out of the ordinary and should be fixed, but can cause a failure.
- **ERROR:** These events can cause a failure in a specific part of the application and require urgent attention.
- **CRITICAL:** These events can cause the whole application to fail and require immediate intervention.

Any logging above the **INFO** level will trigger a [Sentry](http://sentry.io) issue and alert the Core Developer team.

## Draft Pull Requests

Github [provides a PR feature](https://github.blog/2019-02-14-introducing-draft-pull-requests/) that allows the PR author to mark it as a Draft when opening it. This provides both a visual and functional indicator that the contents of the PR are in a draft state and not yet ready for formal review.

This feature should be utilized in place of the traditional method of prepending `[WIP]` to the PR title.
