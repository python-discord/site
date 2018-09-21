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
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
COPY . .

RUN apt-get purge -y \
            gcc \
            libc-dev \
            libpq-dev

CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
