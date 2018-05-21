from rethinkdb import ReqlOpFailedError


def run(db, table, table_obj):
    """
    Create a secondary index on the "snowflake" key, so we can easily get documents by matching that key
    """

    try:
        db.run(db.query(table).index_create("snowflake"))
        db.run(db.query(table).index_wait("snowflake"))
    except ReqlOpFailedError:
        print("Index already exists.")
