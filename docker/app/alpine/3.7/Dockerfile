FROM python:3.7-alpine

STOPSIGNAL SIGQUIT
ARG EXTRAS=deploy

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
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS] \
    && apk del --purge build

COPY . .
RUN SECRET_KEY=abc DATABASE_URL=postgresql://fake:password@host/database python manage.py collectstatic

CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
