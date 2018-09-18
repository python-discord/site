FROM python:3.6-alpine

ARG EXTRAS=deploy

RUN apk add \
        gcc \
        libpq \
        musl-dev

WORKDIR /app
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
COPY . .

RUN apk del \
        gcc

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
