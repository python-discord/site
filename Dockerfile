FROM --platform=linux/amd64 python:3.9-slim-buster

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install -U poetry

# Copy the project files into working directory
WORKDIR /app

# Install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

ENV GIT_SHA=$git_sha
ENV PARENT_HOST=replace_me.host

# Copy the source code in last to optimize rebuilding the image
COPY . .

RUN SECRET_KEY=dummy_value python manage.py distill-local build --traceback --force --collectstatic
