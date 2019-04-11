FROM bitnami/python:3.7-prod

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

COPY Pipfile Pipfile.lock /app/

RUN rm -r /opt/bitnami/python/lib/python3.*/site-packages/setuptools* && \
    pip install --no-cache-dir -U setuptools

RUN python3 -m pip install pipenv \
    && python3 -m pipenv install --system --deploy \
    && pip install uwsgi==2.0.18

COPY . .

RUN SECRET_KEY=placeholder DATABASE_URL=sqlite:// python3 manage.py collectstatic --no-input --clear --verbosity 0

RUN apt-get purge -y \
            gcc \
            libc-dev \
            libpq-dev

CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
