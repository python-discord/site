FROM python:3.7-stretch

ARG EXTRAS=deploy

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

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
