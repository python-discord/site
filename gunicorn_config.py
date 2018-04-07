# coding=utf-8
def when_ready(_server):
    """ server hook that only runs when the gunicorn master process loads """

    print("Creating tables...")

    from pysite.database import RethinkDB

    db = RethinkDB(loop_type=None)
    created = db.create_tables()

    print(f"Created {created} tables.")
