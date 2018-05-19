from rethinkdb import ReqlOpFailedError


def run(db, table, table_obj):
    try:
        db.run(db.query(table).index_create("snowflake"))
        db.run(db.query(table).index_wait("snowflake"))
    except ReqlOpFailedError:
        print("Index already exists.")
