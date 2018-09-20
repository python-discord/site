FROM python:3.7-alpine

ARG EXTRAS=deploy

RUN adduser \
    --disabled-login \
    --no-create-home \
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
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
RUN apk del --purge build

COPY . .

USER pysite
CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
