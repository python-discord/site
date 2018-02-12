# coding=utf-8

from flask import g, jsonify, session

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
        api_key = session.get('api_key')

        if self.validate_key(api_key):
            if tag_name:
                data = rdb.get(tag_name).run(g.db.conn)
                data = dict(data) if data else {}
            else:
                data = rdb.pluck('tag_name').run(g.db.conn)
                data = list(data) if data else []
        else:
            data = {'errors': 'invalid api_key'}

        return jsonify(data)

    def post(self):

        rdb = rethinkdb.table(self.table)
        tag_name = session.get('tag_name')
        tag_content = session.get('tag_content')
        tag_category = session.get('tag_category')
        api_key = session.get('api_key')

        if self.validate_key(api_key):
            if tag_name and tag_content:
                rdb.insert({
                    'tag_name': tag_name,
                    'tag_content': tag_content,
                    'tag_category': tag_category
                }).run(g.db.conn)
                data = {'errors': None}

            else:
                required = {'tag_name': tag_name, 'tag_content': tag_content}
                missing = [key for key, value in required.items() if not value]
                s = 's' if len(missing) > 1 else ''
                error = f"Missing {len(missing)} required parameter{s}: {', '.join(missing)}"
                data = {'errors': error}

        else:
            data = {'errors': 'invalid api_key'}

        return jsonify(data)
