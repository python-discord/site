FROM python:3.7-slim

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    PIPENV_HIDE_EMOJIS=1 \
    PIPENV_NOSPIN=1

# Create non-root user.
RUN useradd --system --shell /bin/false --uid 1500 pysite

# Install pipenv & pyuwsgi
RUN pip install -U pipenv pyuwsgi

# Copy the project files into working directory
WORKDIR /app
COPY . .

# Install project dependencies
RUN pipenv install --system --deploy

# Migrate, collect and start the app
RUN chmod +x /app/docker/app/scripts/migrate.sh
ENTRYPOINT ["/app/docker/app/scripts/migrate.sh"]
CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
