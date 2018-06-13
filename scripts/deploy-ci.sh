#!/bin/bash

# Build and deploy on master branch
if [[ $CI_COMMIT_REF_SLUG == 'master' ]]; then
    echo "Connecting to docker hub"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

    changed_lines=$(git diff HEAD~1 HEAD docker/ci.Dockerfile | wc -l)

    if [ $changed_lines != '0' ]; then
      echo "ci.Dockerfile was changed"

      echo "Building CI container"
      docker build -t pythondiscord/site-ci:latest -f docker/ci.Dockerfile .

      echo "Pushing image to Docker Hub"
      docker push pythondiscord/site-ci:latest
    else
      echo "ci.Dockerfile was not changed, not building"
    fi
else
    echo "Skipping CI Docker build"
fi
