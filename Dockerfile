FROM python:3.8-slim-buster

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    PIPENV_HIDE_EMOJIS=1 \
    PIPENV_NOSPIN=1

# Install pipenv
RUN pip install -U pipenv

# Copy the project files into working directory
WORKDIR /app

# Copy dependency files
COPY Pipfile Pipfile.lock ./

# Install project dependencies
RUN pipenv install --system --deploy

# Copy project code
COPY . .

# Set Git SHA environment variable
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Run web server through custom manager
ENTRYPOINT ["python", "manage.py"]
CMD ["run"]
