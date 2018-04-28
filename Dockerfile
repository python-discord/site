FROM pythondiscord/site-base:latest

RUN pip install pipenv

RUN mkdir /site
COPY . /site
WORKDIR /site
ENV PYTHONPATH=/site

RUN pipenv sync

EXPOSE 10012

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["pipenv", "run", "gunicorn", "-w", "12", "-b", "0.0.0.0:10012", "-c", "gunicorn_config.py", "--log-level", "info", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "app:app"]
