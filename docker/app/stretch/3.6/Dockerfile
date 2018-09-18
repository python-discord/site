FROM python:3.6-stretch

ARG EXTRAS=deploy

RUN apt-get update -y
RUN apt-get install -y \
                automake \
                cmake \
                gcc \
                libc-dev \
                libpq-dev


WORKDIR /app
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
COPY . .

RUN apt-get purge -y \
            automake \
            cmake \
            gcc

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
