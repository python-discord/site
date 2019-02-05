FROM python:3.7-alpine

STOPSIGNAL SIGQUIT

RUN adduser \
    -D \
    -H \
    -u 1500 \
    pysite

RUN apk add --no-cache --update --virtual build \
        gcc \
        linux-headers \
        musl-dev \
    && \
        apk add \
        curl \
        postgresql-dev

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
RUN python3 -m pip install poetry \
    && python3 -m poetry install --extras deploy \
    && apk del --purge build

COPY . .

CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
