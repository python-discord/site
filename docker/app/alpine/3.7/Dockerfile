FROM python:3.7-alpine

ARG EXTRAS=deploy

RUN apk add --no-cache --virtual build \
        gcc \
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

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
