FROM python:3.6-stretch

ARG EXTRAS=deploy

RUN adduser \
    --disabled-login \
    --no-create-home \
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
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
COPY . .

RUN apt-get purge -y \
            gcc \
            libc-dev \
            libpq-dev

USER pysite
CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
