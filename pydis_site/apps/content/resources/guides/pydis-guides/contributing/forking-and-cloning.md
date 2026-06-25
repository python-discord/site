---
title: Forking and Cloning a Repository
description: A guide to forking and cloning repositories on GitHub.
icon: fab fa-github
---

We develop our projects on GitHub, which is a platform for hosting and collaborating on code.
In order to run our projects yourself, you will need a local copy of the relevant repository on your computer.

As you do not have write access directly to our repositories, you will first need to create a fork of the repository,
which is your own repository on GitHub. This will allow you to push changes to a branch on your fork, and create a
pull request to propose your changes to the main repository.

After you have created a fork, you will then need to clone the repository to your computer, which is the process
of downloading the repository from GitHub to your local machine. You will need Git installed on your computer to do this.

The following will use the [Sir-Lancebot](https://github.com/python-discord/sir-lancebot/) repository as an example, but the steps are the same for all other repositories.

See our [working with Git guide](./working-with-git) for more information on how to work with Git.

# Forking a Repository

*Note: Members of the Python Discord staff can create feature branches directly on the repository without forking it.*

1. Navigate to the repository page on GitHub and press the `Fork` button at the top of the page.
![Github Fork Button](/static/images/content/contributing/fork_button.png)
2. Fork it to your account.<br>
![Github Fork to User](/static/images/content/contributing/fork_user.png)
3. Later, you will need the Git URL of your forked repository in order to clone it.
In your newly forked repository, copy the Git URL by clicking the green `Code` button, then click the Copy Link button.
![Github Fork Clone URL](/static/images/content/contributing/fork_clone.png)

> If you have SSH set up with GitHub, you may instead click the `SSH` button above the Copy Link button to get the SSH URL.

# Cloning a Repository

You can clone a repository using the command line directly, or by using your IDEs built-in Git integration. We will cover how to do this with the command line, and with PyCharm's integration.

## Cloning with the command line

1. Clone your forked repository using `git clone` followed by your fork's Git URL. Then, change your working directory to the repository.

```shell
$ git clone https://github.com/<your username>/sir-lancebot
...
$ cd sir-lancebot
```

## Cloning with PyCharm

1. Load up PyCharm and click `Get from VCS`.<br>
   ![Create Project in PyCharm](/static/images/content/contributing/pycharm_create_project.png)
2. Enter the URL of your forked repository.
3. Change the directory if you desire and click `Clone`.<br>
   ![Clone Git Project in Pycharm](/static/images/content/contributing/pycharm_checkout.png)
