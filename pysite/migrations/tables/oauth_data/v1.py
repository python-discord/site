def run(db, table, table_obj):
    db.run(db.query(table).index_create("snowflake"))
    db.run(db.query(table).index_wait("snowflake"))
