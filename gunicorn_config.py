# coding=utf-8
def when_ready(server):
    """ server hook that only runs when the gunicorn master process loads """

    server.log.info("Creating tables...")

    from pysite.database import RethinkDB

    db = RethinkDB(loop_type=None)
    created = db.create_tables()

    server.log.info(f"Created {created} tables.")
