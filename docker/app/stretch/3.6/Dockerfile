FROM python:3.6-stretch

STOPSIGNAL SIGQUIT
ARG EXTRAS=deploy

RUN adduser \
    --disabled-login \
    --no-create-home \
    --uid 1500 \
    pysite

RUN apt-get update -y \
    && \
        apt-get install --no-install-recommends -y \
                gcc \
                libc-dev \
                libpq-dev \
    && \
        apt-get clean \
    && \
        rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN python3 -m pip install pipenv \
    && python3 -m pipenv install --dev --system --deploy

COPY . .

RUN python3 manage.py collectstatic --no-input --clear

RUN apt-get purge -y \
            gcc \
            libc-dev \
            libpq-dev

CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
