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
          Our community-driven Discord bot.
        </div>
        <div class="tags has-addons">
          <span class="tag is-dark">Difficulty</span>
          <span class="tag is-primary">Beginner</span>
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
          The community and moderation Discord bot.
        </div>
        <div class="tags has-addons">
          <span class="tag is-dark">Difficulty</span>
          <span class="tag is-warning">Intermediate</span>
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
          The website, subdomains and API.
        </div>
        <div class="tags has-addons">
          <span class="tag is-dark">Difficulty</span>
          <span class="tag is-danger">Advanced</span>
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
  Unsure of what contributing to open source projects involves? Have questions about how to use GitHub? Just need to know about our contribution etiquette? Completing these steps will have you ready to make your first contribution.

  Feel free to skip any steps you're already familiar with, but please make sure not to miss the  [Contributing Guidelines](#5-read-our-contributing-guidelines).

  If you are here looking for the answer to a specific question, check out the sub-articles in the top right of the page to see a list of our guides.

### 1. Learn the basics of Git
  Git is a _Version Control System_, software for carefully tracking changes to the files in a project. Git allows the same project to be worked on by people in different places. You can make changes to your local code and then distribute those changes to the other people working on the project.

  Check out these [**resources to get started using Git**](./working-with-git/).

### 2. Fork the repo
  GitHub is a website based on the Git version control system that stores project files in the cloud. The people working on the project can use GitHub as a central place for sending their changes, getting their teammates' changes, and communicating with each other. Forking the repository that you want to work on will create a copy under your own GitHub account. You'll make your changes to this copy, then later we can bring them back to the PyDis repository.

  Check out our [**guide on forking a GitHub repo**](./forking-repository/).

### 3. Clone the repo
  Now that you have your own fork you need to be able to make changes to the code. You can clone the repo to your local machine, commit changes to it there, then push those changes to GitHub.

  Check out our [**guide on cloning a GitHub repo**](./cloning-repository/).

### 4. Set up the project
  You have the source code on your local computer, now how do you actually run it? We have detailed guides on setting up the environment for each of our projects:

  * [**Sir Lancebot**](./sir-lancebot/)

  * [**Python Bot**](./bot/)

  * [**Site**](./site/)

### 5. Read our Contributing Guidelines
  We have a few short rules that all contributors must follow. Make sure you read and follow them while working on our projects.

  [**Contributing Guidelines**](./contributing-guidelines/).

  As mentioned in the Contributing Guidelines, we have a simple style guide for our projects based on PEP 8. Give it a read to keep your code consistent with the rest of the codebase.

  [**Style Guide**](./style-guide/)

### 6. Create an issue
  The first step to any new contribution is an issue describing a problem with the current codebase or proposing a new feature. All the open issues are viewable on the GitHub repositories, for instance here is the [issues page for Sir Lancebot](https://github.com/python-discord/sir-lancebot/issues). If you have an idea that you want to implement, open a new issue (and check out our [**guide on writing an issue**](./issues/)). Otherwise you can browse the unassigned issues and ask to be assigned to one that you're interested in, either in the comments on the issue or in the`#dev-contrib`channel on Discord.

  Don't move forward until your issue is approved by a Core Developer. Issues are not guaranteed to be approved so your work may be wasted.
  {: .notification .is-warning }

### 7. Open a pull request
  After your issue has been approved and you've written your code and tested it, it's time to open a pull request. Pull requests are a feature in GitHub; you can think of them as asking the project maintainers to accept your changes. This gives other contributors a chance to review your code and make any needed changes before it's merged into the main branch of the project.

  Check out our [**Pull Request Guide**](./contributing/pull-requests/) for help with opening a pull request and going through the review process.

  Check out our [**Code Review Guide**](../code-reviews-primer/) to learn how to be a star reviewer. Reviewing PRs is a vital part of open source development, and we always need more reviewers!

### That's it!
Thank you for contributing to our community projects. If you don't understand anything or need clarification, feel free to ask a question in the`dev-contrib`channel and keep an eye out for staff members with the **@PyDis Core Developers** role in the server. We're always happy to help!
