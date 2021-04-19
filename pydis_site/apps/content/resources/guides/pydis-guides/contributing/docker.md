---
title: Working with Docker & Docker Compose
description: Guide to running our projects with Docker and Docker CE.
icon: fab fa-docker
---

Both our [Site](../site/) and [Bot](../bot/) projects use Docker and Docker-Compose during development in order to provide an easy to setup and consistent development environment.

Consider reading some of the following topics if you're interested in learning more about Docker itself:

 * [**What is Docker?**](https://docs.docker.com/engine/docker-overview/)
 * [**How can I learn to use it for my own stuff?**](https://docs.docker.com/get-started/)
 * [**What about Docker Compose, what's it for?**](https://docs.docker.com/compose/)

# Docker Installation
You can find installation guides available for your respective OS from the official Docker documentation:
[https://docs.docker.com/install/](https://docs.docker.com/install/)

## After Installing on Linux
If you're on Linux, there's a few extra things you should do:

1. [**Add your user to the `docker` user group so you don't have to use `sudo` when running docker or docker-compose.**](#add-user-group)
2. [**Start up the Docker service.**](#run-the-service)
3. [**Set the Docker service to start on boot.**](#start-on-boot) **(optional)**

### Run the Service
Most linux distributions **systemd**, you can start the service with:
```shell
$ sudo systemctl start docker
```

### Add User Group
```shell
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```
Log out and log back in to ensure your group changes work.

### Start on Boot
```shell
$ sudo systemctl enable docker
```

# Possible Issues
### Couldn't connect to Docker daemon
```shell
ERROR: Couldn't connect to Docker daemon at http+docker://localhost - is it running?
```
**Problem**<br>
Your Docker service is either not started, or you haven't yet installed Docker.

**Solution**<br>
[Start the service](#run-the-service) or ensure it's installed.
If it's not, [install it](#docker-installation).

### Error loading config file
```plaintext
WARNING: Error loading config file: /home/user/.docker/config.json -
stat /home/user/.docker/config.json: permission denied
```
**Problem**<br>
You initially ran Docker using `sudo` before adding your user to the `docker` group, resulting in your `~/.docker/` directory being created with incorrect permissions.

**Solution**<br>
Remove the existing `~/.docker/` directory. It will be automatically re-created with the correct permissions.

### Drive has not been shared (Windows users)

When attempting to run the `docker-compose up` command on a Windows machine, you receive the following or similar error message:
```text
ERROR: for bot_bot_1 Cannot create container for service bot: b'Drive has not been shared'
```
**Problem**<br>
Windows has not been configured to share drives with Docker.

**Solution**<br>
> NOTE: Solution requires Windows user credentials for an account that has administrative privileges.

1. Right-click the Docker icon in the Windows system tray, and choose "Settings" from the context menu.
![Docker Settings](/static/images/content/contributing/docker_settings.webp)

2. Click the "Shared Drives" label at the left, and check the box next to the drive letter where your project is stored.
![Docker Shared Drives](/static/images/content/contributing/docker_shared_drives.webp)

3. Click "Apply" and enter appropriate Windows credentials (likely just your own account, if you have administrative privileges).

4. Re-run the `docker-compose up` command.

# Compose Project Names
When you launch services from a docker-compose, you'll notice the name of the containers aren't just the service name.
You'll see this when launching your compose, as well as being able to be seen in the command `docker-compose ps` which will list the containers.
It should match something like this:
```
site_site_1
```
This matched the following container name format:
```
projectname_servicename_1
```
By default, your project name will match the name of the folder your project is inside in all lowercase.

You can specify a custom project name by adding a `COMPOSE_PROJECT_NAME` variable to your `.env` file before launching the compose:
```
COMPOSE_PROJECT_NAME=site
```
Containers with the same project name end up connected to the same network by default.
For example, the `site` container connects with `postgres` via the matching hostname inside the container.
Even if you didn't expose a port to the host, the two containers would be able to talk to each other.

You can have two different projects able to communicate in the same way by having them use the same project name.
We use this feature to allow the `bot` container to communicate with a separate local copy of `site` that may need to be tested during development.

By default, the `bot` container could launch with a name of `bot_bot_1` and the `site` container with a name of `site_site_1`. Since the prefixes are different, they're in distinct projects, so can't talk with each other.

If we got to the bot's `.env` file, and add the line below, we can set `bot` to run in the same project as `site`:
```
COMPOSE_PROJECT_NAME=site
```
Now they can talk to each other!
