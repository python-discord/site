## Contents
1. [You will learn](#you-will-learn)
2. [Introduction](#introduction)
3. [Installing Docker](#installing-docker)
4. [Creating Dockerfile](#creating-dockerfile)
5. [Building Image and Running Container](#building-image-and-running-container)
6. [Creating Volumes](#creating-volumes)
7. [Using GitHub Actions for full automation](#using-github-actions-for-full-automation)

## You will learn
- how to write Dockerfile
- how to build Docker image and run the container
- how to use docker-compose
- how to make docker keep the files throughout the container's runs
- how to parse environment variables into container
- how to use GitHub Actions for automation
- how to setup self hosted runner
- how to use runner secrets

## Introduction
Let's say you have got a nice discord bot written in python and you have a VPS to host it on. Now the only question is how to run it 24/7. You might have been suggested to use *screen multiplexer*, but it has some disadvantages:
1. Every time you update the bot you have to SSH to your server, attach to screen, shutdown the bot, run `git pull` and run the bot again. You might have good extensions management that allows you to update the bot without restarting it, but there are some other cons as well
2. If you update some dependencies, you have to update them manually
3. The bot doesn't run in an isolated environment, which is not good for security

But there's a nice and easy solution to these problems - **Docker**! Docker is a containerization utility that automates some stuff like dependencies update and running the application in the background. So let's get started.

## Installing Docker
The best way to install the docker is to use the [convenience script](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script) provided by Docker developers themselves. You just need 2 lines:
```shell
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
```

## Creating Dockerfile
To tell Docker what it has to do to run the application, we need to create a file named `Dockerfile` in our project's root.

1. First we need to specify the *base image*. Doing that will make Docker install some apps we need to run our bot, for example the Python interpreter
```dockerfile
FROM python:3.10-bullseye
```
2. Next, we need to copy our requirements to some directory *inside the container*. Let's call it `/app`
```dockerfile
COPY requirements.txt /app/
```
3. Now we need to set the directory as working and install the requirements
```dockerfile
WORKDIR /app
RUN pip install -r requirements.txt
```
4. The only thing that is left to do is to copy the rest of project's files and run the main executable
```dockerfile
COPY . .
CMD ["python3", "main.py"]
```

The final version of Dockerfile looks like this:
```dockerfile
FROM python:3.10-bullseye
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
```

## Building Image and Running Container
Now update the project on your VPS and we can run the bot with Docker.
1. Build the image (dot at the end is very important)
```shell
$ docker build -t mybot .
```
2. Run the container
```shell
$ docker run -d --name mybot mybot:latest
```
3. Read bot logs (keep in mind that this utility only allows to read STDERR)
```shell
$ docker logs -f mybot
```
If everything went successfully, your bot will go online and will keep running!

## Using docker-compose
Just 2 commands to run a container is cool but we can shorten it down to just 1 simple command. For that, create a `docker-compose.yml` file in project's root and fill it with the following contents:
```yml
version: "3.8"
services:
  main:
    build: .
    container-name: mybot
```
Update the project on VPS, remove the previous container with `docker rm -f mybot` and run this command
```shell
docker-compose up -d --build
```
Now the docker will automatically build the image for you and run the container.

## Creating Volumes
The files creating during container run are destroyed after its recreation. To prevent some files from getting destroyed, we need to use *volumes* that basically save the files from directory inside of container somewhere on drive.
1. Create a new directory somewhere and copy path to it
```shell
$ mkdir mybot-data && echo $(pwd)/mybot-data
```
My path is `/home/exenifix/mybot-data`, yours is most likely different.
2. In your project, store the files that need to be persistant in a separate directory (eg. `data`)
3. Add the `volumes` construction to `docker-compose` so it looks like this:
```yml
version: "3.8"
services:
  main:
    build: .
    container-name: mybot
    volumes:
      - /home/exenifix/mybot-data:/app/data
```
The path before the colon `:` is the directory *on drive* and the second path is the directory *inside of container*. All the files saved in container in that directory will be saved on drive's directory as well and Docker will be accessing them *from drive*.

## Using GitHub Actions for full automation
Now it's time to fully automate the process and make Docker update the bot automatically on every commit or release. For that, we will use a **GitHub Actions workflow**, which basically runs some commands when we need to. You may read more about them [here](https://docs.github.com/en/actions/using-workflows).

### Create repository secret
We will not have the ability to use `.env` files with the workflow, so it's better to store the environment variables as **actions secrets**.
1. Head to your repository page -> Settings -> Secrets -> Actions
2. Press `New repository secret`
3. Give it a name like `TOKEN` and paste the value
Now we will be able to access its value in workflow like `${{ secrets.TOKEN }}`. However, we also need to parse the variable into container now. Edit `docker-compose` so it looks like this:
```yml
version: "3.8"
services:
  main:
    build: .
    container-name: mybot
    volumes:
      - /home/exenifix/mybot-data:/app/data
    environment:
      - TOKEN
```

### Setup self-hosted runner
To run the workflow on our VPS, we will need to register it as *self hosted runner*.
1. Head to Settings -> Actions -> Runners
2. Press `New self-hosted runner`
3. Select runner image and architecture
4. Follow the instructions but don't run the runner
5. Instead, create a service
```shell
$ sudo ./svc.sh install
$ sudo ./svc.sh start
```
Now we have registered our VPS as a self-hosted runner and we can run the workflow on it now.

### Write a workflow
Create a new file `.github/workflows/runner.yml` and paste the following content into it (it is easy to understand so I am not going to give many comments)
```yml
name: Docker Runner

on:
  push:
    branches: [ master ]

jobs:
  run:
    runs-on: self-hosted
    environment: production

    steps:
      - uses: actions/checkout@v3

      - name: Run Container
        run: docker-compose up -d --build
        env:
          TOKEN: ${{ secrets.TOKEN }}

      - name: Cleanup Unused Images
        run: docker image prune -f
```

Run `docker rm -f mybot` (it only needs to be done once) and push to GitHub. Now if you open `Actions` tab on your repository, you should see a workflow running your bot. Congratulations!

### Displaying logs in actions terminal
There's a nice utility for reading docker container's logs and stopping upon meeting a certain phrase and it might be useful for you as well.
1. Install the utility on your VPS with
```shell
$ pip install exendlr
```
2. Add a step to your workflow that would show the logs until it meets `"ready"` phrase. I recommend putting it before the cleanup.
```yml
- name: Display Logs
  run: python3 -m exendlr mybot "ready"
```
Now you should see the logs of your bot until the stop phrase is met. 

**WARNING**
> The utility only reads from STDERR and redirects to STDERR, if you are using STDOUT for logs, it will not work and will be waiting for stop phrase forever. The utility automatically exits if bot's container is stopped (eg. error occured during starting) or if a log line contains a stop phrase. Make sure that your bot 100% displays a stop phrase when it's ready otherwise your workflow will get stuck.
