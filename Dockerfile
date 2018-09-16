FROM python:3.7-alpine

RUN apk add git libpq postgresql-dev gcc cmake autoconf automake musl-dev

COPY . /app
WORKDIR /app

RUN python3 -m pip install .[deploy]
RUN apk del git gcc cmake autoconf automake

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
