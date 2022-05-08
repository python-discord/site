---
title: Contributing
description: A guide to contributing to our open source projects.
icon: fab fa-github
---

Our projects on Python Discord are open source and [available on GitHub](https://github.com/python-discord).  If you would like to contribute, consider one of the following projects:

<!-- Project cards -->
<div class="columns is-multiline is-centered is-3 is-variable">
  <div class="column is-one-third-desktop is-half-tablet">
    <div class="card github-card">
      <div class="card-header">
        <div class="card-header-title is-centered">
          <a class="is-size-5" href="https://github.com/python-discord/sir-lancebot">
            <i class="fab fa-github"></i>&ensp;<strong >Sir Lancebot</strong>
          </a>
        </div>
      </div>
      <div class="card-content">
        <div class="content">
          Sir Lancebot has a collection of self-contained, for-fun features. If you're new to Discord bots or contributing, this is a great place to start!
        </div>
      </div>
      <div class="card-footer">
        <a href="https://github.com/python-discord/sir-lancebot/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc" class="card-footer-item"><i class="fas fa-exclamation-circle"></i>&ensp;Issues</a>
        <a href="https://github.com/python-discord/sir-lancebot/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc" class="card-footer-item"><i class="fas fa-code-merge"></i>&ensp;PRs</a>
      </div>
      <div class="card-footer">
        <a href="/pages/guides/pydis-guides/contributing/sir-lancebot" class="card-footer-item"><i class="fas fa-cogs"></i>&ensp;Setup and Configuration Guide</a>
      </div>
    </div>
  </div>
  <div class="column is-one-third-desktop is-half-tablet">
    <div class="card github-card">
      <div class="card-header">
        <div class="card-header-title is-centered">
          <a href="https://github.com/python-discord/bot">
            <strong class="is-size-5"><i class="fab fa-github"></i>&ensp;Bot</strong>
          </a>
        </div>
      </div>
      <div class="card-content">
        <div class="content">
          Called @Python on the server, this bot handles moderation tools, help channels, and other critical features for our community.
        </div>
      </div>
      <div class="card-footer">
        <a href="https://github.com/python-discord/bot/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc" class="card-footer-item"><i class="fas fa-exclamation-circle"></i>&ensp;Issues</a>
        <a href="https://github.com/python-discord/bot/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc" class="card-footer-item"><i class="fas fa-code-merge"></i>&ensp;PRs</a>
      </div>
      <div class="card-footer">
        <a href="/pages/guides/pydis-guides/contributing/bot" class="card-footer-item"><i class="fas fa-cogs"></i>&ensp;Setup and Configuration Guide</a>
      </div>
    </div>
  </div>
  <div class="column is-one-third-desktop is-half-tablet">
    <div class="card github-card">
      <div class="card-header">
        <div class="card-header-title is-centered">
          <a href="https://github.com/python-discord/site">
            <strong class="is-size-5"><i class="fab fa-github"></i>&ensp;Site</strong>
          </a>
        </div>
      </div>
      <div class="card-content">
        <div class="content">
          This website itself! This project is built with Django and includes our API, which is used by various services such as @Python.
        </div>
      </div>
      <div class="card-footer">
        <a href="https://github.com/python-discord/site/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc" class="card-footer-item"><i class="fas fa-exclamation-circle"></i>&ensp;Issues</a>
        <a href="https://github.com/python-discord/site/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc" class="card-footer-item"><i class="fas fa-code-merge"></i>&ensp;PRs</a>
      </div>
      <div class="card-footer">
        <a href="/pages/guides/pydis-guides/contributing/site" class="card-footer-item"><i class="fas fa-cogs"></i>&ensp;Setup and Configuration Guide</a>
      </div>
    </div>
  </div>
</div>

# How do I start contributing?
Unsure of what contributing to open source projects involves? Have questions about how to use GitHub? Just need to know about our contribution etiquette? Completing these steps will have you ready to make your first contribution no matter your starting point.

Feel free to skip any steps you're already familiar with, but please make sure not to miss the [Contributing Guidelines](#5-read-our-contributing-guidelines).

If you are here looking for the answer to a specific question, check out the sub-articles in the top right of the page to see a list of our guides.

**Note:** We use Git to keep track of changes to the files in our projects. Git allows you to make changes to your local code and then distribute those changes to the other people working on the project. You'll use Git in a couple steps of the contributing process. You can refer to this [**guide on using Git**](./working-with-git/).
{: .notification }

### 1. Fork and clone the repo
GitHub is a website based on Git that stores project files in the cloud. We use GitHub as a central place for sending changes, reviewing others' changes, and communicating with each other. You'll need to create a copy under your own GitHub account, a.k.a. "fork" it. You'll make your changes to this copy, which can then later be merged into the Python Discord repository.

*Note: Members of the Python Discord staff can create feature branches directly on the repo without forking it.*

Check out our [**guide on forking a GitHub repo**](./forking-repository/).

Now that you have your own fork you need to be able to make changes to the code. You can clone the repo to your local machine, commit changes to it there, then push those changes to GitHub.

Check out our [**guide on cloning a GitHub repo**](./cloning-repository/).

### 2. Set up the project
You have the source code on your local computer, now how do you actually run it? We have detailed guides on setting up the environment for each of our main projects:

* [**Sir Lancebot**](./sir-lancebot/)

* [**Python Bot**](./bot/)

* [**Site**](./site/)

### 3. Read our Contributing Guidelines
We have a few short rules that all contributors must follow. Make sure you read and follow them while working on our projects.

[**Contributing Guidelines**](./contributing-guidelines/).

As mentioned in the Contributing Guidelines, we have a simple style guide for our projects based on PEP 8. Give it a read to keep your code consistent with the rest of the codebase.

[**Style Guide**](./style-guide/)

### 4. Create an issue
The first step to any new contribution is an issue describing a problem with the current codebase or proposing a new feature. All the open issues are viewable on the GitHub repositories, for instance here is the [issues page for Sir Lancebot](https://github.com/python-discord/sir-lancebot/issues). If you have something that you want to implement open a new issue to present your idea. Otherwise you can browse the unassigned issues and ask to be assigned to one that you're interested in, either in the comments on the issue or in the [`#dev-contrib`](https://discord.gg/2h3qBv8Xaa) channel on Discord.

[**How to write a good issue**](./issues/)

Don't move forward until your issue is approved by a Core Developer. Issues are not guaranteed to be approved so your work may be wasted.
{: .notification .is-warning }

### 5. Open a pull request
After your issue has been approved and you've written your code and tested it, it's time to open a pull request. Pull requests are a feature in GitHub; you can think of them as asking the project maintainers to accept your changes. This gives other contributors a chance to review your code and make any needed changes before it's merged into the main branch of the project.

Check out our [**Pull Request Guide**](./pull-requests/) for help with opening a pull request and going through the review process.

Check out our [**Code Review Guide**](../code-reviews-primer/) to learn how to be a star reviewer. Reviewing PRs is a vital part of open source development, and we always need more reviewers!

### That's it!
Thank you for contributing to our community projects. If there's anything you don't understand or you just want to discuss with other contributors, come visit the [`#dev-contrib`](https://discord.gg/2h3qBv8Xaa) channel to ask questions. Keep an eye out for staff members with the **@PyDis Core Developers** role in the server; we're always happy to help!
