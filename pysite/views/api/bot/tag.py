# coding=utf-8
__author__ = 'Ferret Moles'

from flask import g, session

from pysite.base_route import APIView

import rethinkdb


class TagView(APIView):
    path = '/tag'
    name = 'tag'
    table = 'tag'

    def __init__(self):

        # make sure the table exists
        conn = g.db.get_connection()
        try:
            rethinkdb.db(g.db.database).table_create(self.table).run(conn)
        except rethinkdb.RqlRuntimeError:
            print(f'Table {self.table} exists')
        conn.close()

    def get(self):

        tag_name = session.get('tag_name')

        if tag_name:
            pass  # get that specific tag
        else:
            pass  # get a list of all tags

        return

    def post(self):

        tag_name = session.get('tag_name')
        tag_content = session.get('tag_content')

        if tag_name and tag_content:
            pass       # put the data in the database
            return     # some sort of success message
        else:
            return     # abort?
