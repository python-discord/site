FROM python:3.6-stretch

ARG EXTRAS=deploy

RUN apt-get update -y
RUN apt-get install -y \
                autoconf \
                automake \
                cmake \
                gcc \
                git \
                libc-dev \
                libpq-dev


COPY . /app
WORKDIR /app
RUN python3 -m pip install .[$EXTRAS]

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
