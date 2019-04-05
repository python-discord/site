FROM python:3.6-alpine

STOPSIGNAL SIGQUIT
ARG EXTRAS=deploy

RUN adduser \
    -D \
    -H \
    -u 1500 \
    pysite

RUN apk add --no-cache --virtual build \
        gcc \
        linux-headers \
        musl-dev \
    && \
        apk add --no-cache \
        curl \
        postgresql-dev

WORKDIR /app

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN python3 -m pip install pipenv \
    && python3 -m pipenv install --dev --system --deploy \
    && apk del --purge build

COPY . .

RUN python3 manage.py collectstatic --no-input --clear

CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
