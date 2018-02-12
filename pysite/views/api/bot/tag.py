# coding=utf-8
__author__ = 'Ferret Moles'

from flask import g, session, jsonify

import rethinkdb

from pysite.base_route import APIView


class TagView(APIView):
    path = '/tag'
    name = 'tag'
    table = 'tag'

    def __init__(self):

        # make sure the table exists
        conn = g.db.get_connection()
        try:
            rethinkdb.db(g.db.database).table_create(self.table, {'primary_key': 'tag_name'}).run(conn)
        except rethinkdb.RqlRuntimeError:
            print(f'Table {self.table} exists')
        conn.close()

    def get(self):

        rdb = rethinkdb.table(self.table)
        tag_name = session.get('tag_name')

        if tag_name:
            tag_data = rdb.get(tag_name).run(g.db.conn)
            tag_data = dict(tag_data) if tag_data else {}
        else:
            tag_data = rdb.pluck('tag_name').run(g.db.conn)
            tag_data = list(tag_data) if tag_data else []

        return jsonify(tag_data)

    def post(self):

        tag_name = session.get('tag_name')
        tag_content = session.get('tag_content')

        if tag_name and tag_content:
            pass       # put the data in the database
            return     # some sort of success message
        else:
            return     # abort?
