def when_ready(server):
    """ server hook that only runs when the gunicorn master process loads """

    import traceback
    import rethinkdb as r

    try:
        server.log.info("rethinkdb initialising")

        DB_HOST = os.environ.get("RETHINKDB_HOST")
        DB_PORT = os.environ.get("RETHINKDB_PORT")
        DB_DATABASE = os.environ.get("RETHINKDB_DATABASE")
        DB_TABLE = os.environ.get("RETHINKDB_TABLE")
        indexes = ['test']

        conn = r.connect(host=DB_HOST, port=DB_PORT, db=DB_DATABASE)

        # Check if database exists, if not create it
        db_exists = r.db_list().contains(DB_DATABASE).run(conn)
        
        if not db_exists:
            server.log.info('adding database {0}'.format(DB_DATABASE))
            r.db_create(DB_DATABASE).run(conn)

        # Check if table exist, if not create it
        table_exists = r.db(DB_DATABASE).table_list().contains(DB_TABLE).run(conn)
        
        if not table_exists:
            server.log.info('adding table {0}'.format(DB_TABLE))
            r.db(DB_DATABASE).table_create(DB_TABLE).run(conn)

        # Check if index exists if not add it
        rtable = r.db(DB_DATABASE).table(DB_TABLE)
        current_indexes = rtable.index_list().run(conn)
        
        for index in indexes:
            if index not in current_indexes:
                server.log.info('adding index {0}'.format(index))
                rtable.index_create(index).run(conn)

        server.log.info("rethinkdb ready")

    except Exception as e:
        server.log.error(traceback.format_exc())
        server.log.error("rethinkdb failed to initialise")
