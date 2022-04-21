---
title: Pull Requests
description: A guide for opening pull requests.
---

As stated in our [Contributing Guidelines](../contributing-guidelines/), do not open a pull request if you aren't assigned to an approved issue. You can check out our [Issues Guide](../issues/) for help with opening an issue or getting assigned to an existing one.
{: .notification .is-warning }

Before opening a pull request you should have:

1. Committed your changes to your local repository
2. [Linted](../linting/) your code
3. Tested your changes
4. Pushed the branch to your fork of the project on GitHub

## Opening a Pull Request

Navigate to your fork on GitHub and make sure you're on the branch with your changes. Click on `Contribute` and then `Open pull request`:

![Pull Request UI](/static/images/content/contributing/pull_request.png)

In the page that it opened, write an overview of the changes you made and why. This should explain how you resolved the issue that spawned this PR and highlight any differences from the proposed implementation. You should also [link the issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue).

At this stage you can also request reviews from individual contributors. If someone showed interest in the issue or has specific knowledge about it, they may be a good reviewer. It isn't necessary to request your reviewers; someone will review your PR either way.

## The Review Process

Before your changes are merged, your PR needs to be reviewed by other contributors. They will read the issue and your description of your PR, look at your code, test it, and then leave comments on the PR if they find any problems, possibly with suggested changes. Sometimes this can feel intrusive or insulting, but remember that the reviewers are there to help you make your code better.

#### If the PR is already open, how do I make changes to it?

A pull request is between a source branch and a target branch. Updating the source branch with new commits will automatically update the PR to include those commits; they'll even show up in the comment thread of the PR. Sometimes for small changes the reviewer will even write the suggested code themself, in which case you can simply accept them with the click of a button.

If you truly disagree with a reviewer's suggestion, leave a reply in the thread explaining why or proposing an alternative change. Also feel free to ask questions if you want clarification about suggested changes or just want to discuss them further.

## Draft Pull Requests

GitHub [provides a PR feature](https://github.blog/2019-02-14-introducing-draft-pull-requests/) that allows the PR author to mark it as a draft when opening it. This provides both a visual and functional indicator that the contents of the PR are in a draft state and not yet ready for formal review. This is helpful when you want people to see the changes you're making before you're ready for the final pull request.

This feature should be utilized in place of the traditional method of prepending `[WIP]` to the PR title.
