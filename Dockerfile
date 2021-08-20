FROM python:3.9.5-slim-buster

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

# Set Git SHA environment variable
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Copy the source code in last to optimize rebuilding the image
COPY . .

# Run web server through custom manager
ENTRYPOINT ["python", "manage.py"]
CMD ["run"]
