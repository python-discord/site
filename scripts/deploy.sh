#!/bin/bash

cd ..

# Build and deploy on master branch, only if not a pull request
if [[ ($BUILD_SOURCEBRANCHNAME == 'master') && ($SYSTEM_PULLREQUEST_PULLREQUESTID == '') ]]; then
    changed_lines=$(git diff HEAD~1 HEAD docker/Dockerfile.base | wc -l)

    if [ $changed_lines != '0' ]; then
      echo "Dockerfile.base was changed"

      echo "Building site base"
      docker build -t pythondiscord/site-base:latest -f docker/Dockerfile.base .

      echo "Pushing image to Docker Hub"
      docker push pythondiscord/site-base:latest
    else
      echo "Dockerfile.base was not changed, not building"
    fi

    echo "Building image"
    docker build -t pythondiscord/site:latest -f docker/Dockerfile .

    echo "Pushing image"
    docker push pythondiscord/site:latest

    echo "Deploying container"
    curl -H "token: $1" $2
else
    echo "Skipping deploy"
fi
