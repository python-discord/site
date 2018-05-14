import re

from pysite.migrations.runner import run_migrations

STRIP_REGEX = re.compile(r"<[^<]+?>")
WIKI_TABLE = "wiki"


def when_ready(server=None):
    _when_ready(server=server)


def _when_ready(server=None, output_func=None):
    """ server hook that only runs when the gunicorn master process loads """

    if server:
        output = server.log.info
    elif output_func:
        output = output_func
    else:
        output = print

    output("Creating tables...")

    from pysite.database import RethinkDB

    db = RethinkDB(loop_type=None)
    db.conn = db.get_connection()

    # Create any table that doesn't exist
    created = db.create_tables()
    if created:
        tables = ", ".join([f"{table}" for table in created])
        output(f"Created the following tables: {tables}")

    run_migrations(db, output=output)
