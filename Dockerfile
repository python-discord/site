FROM pythondiscord/site-base:latest

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_NOSPIN=1
ENV PIPENV_HIDE_EMOJIS=1

RUN pip install pipenv

RUN mkdir /site
COPY . /site
WORKDIR /site
ENV PYTHONPATH=/site

RUN pipenv sync

EXPOSE 10012

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["pipenv", "run", "gunicorn", "-w", "12", "-b", "0.0.0.0:10012", "-c", "gunicorn_config.py", "--log-level", "info", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "app:app"]
