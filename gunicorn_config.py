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
    db.conn = db.get_connection()

    # Create any table that doesn't exist
    created = db.create_tables()
    if created:
        tables = ", ".join([f"{table}" for table in created])
        output(f"Created the following tables: {tables}")

    # Init the tables that require initialization
    initialized = db.init_tables()
    if initialized:
        tables = ", ".join([f"{table} ({count} items)" for table, count in initialized.items()])
        output(f"Initialized the following tables: {tables}")
