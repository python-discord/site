# coding=utf-8
def when_ready(server=None):
    """ server hook that only runs when the gunicorn master process loads """

    if server:
        output = server.log.info
    else:
        output = print

    output("Creating tables...")

    from pysite.database import RethinkDB

    db = RethinkDB(loop_type=None)
    created = db.create_tables()

    output(f"Created {created} tables.")


if __name__ == "__main__":
    when_ready()
