def when_ready(server):
    """ server hook that only runs when the gunicorn master process loads """

    import traceback
    import rethinkdb as r

    try:
        server.log.info("rethinkdb initialising")

        construct = [
            {'DB': 'test', 'TABLE': 'test', 'INDEXES': ['test']},
        ]
        for struct in construct:
            DB = struct['DB']
            TABLE = struct['TABLE']
            INDEXES = struct['INDEXES']

            conn = r.connect(host='pdrdb', port=28016, db=DB)

            # Check if database exists, if not create it
            db_exists = r.db_list().contains(DB).run(conn)
            if not db_exists:
                server.log.info('adding database {0}'.format(DB))
                r.db_create(DB).run(conn)

            # Check if table exist, if not create it
            table_exists = r.db(DB).table_list().contains(TABLE).run(conn)
            if not table_exists:
                server.log.info('adding table {0}'.format(TABLE))
                result = r.db(DB).table_create(TABLE).run(conn)

            # Check if index exists if not add it
            rtable = r.db(DB).table(TABLE)
            current_indexes = rtable.index_list().run(conn)
            for index in INDEXES:
                if index not in current_indexes:
                    server.log.info('adding index {0}'.format(index))
                    rtable.index_create(index).run(conn)

        server.log.info("rethinkdb ready")

    except Exception as e:
        server.log.error(traceback.format_exc())
        server.log.error("rethinkdb failed to initialise")
