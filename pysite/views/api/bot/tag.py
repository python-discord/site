# coding=utf-8

from flask import g, jsonify, request

import rethinkdb

from pysite.base_route import APIView
from pysite.constants import ErrorCodes


class TagView(APIView):
    path = '/tag'
    name = 'tag'
    table = 'tag'

    def __init__(self):
        # make sure the table exists
        with g.db.get_connection() as conn:
            try:
                rethinkdb.db(g.db.database).table_create(self.table, {'primary_key': 'tag_name'}).run(conn)
            except rethinkdb.RqlRuntimeError:
                print(f'Table {self.table} exists')

    def get(self):
        """
        Indata must be provided as params,
        API key must be provided as header
        """
        rdb = rethinkdb.table(self.table)
        api_key = request.headers.get('X-API-Key')
        tag_name = request.args.get('tag_name')

        if self.validate_key(api_key):
            if tag_name:
                data = rdb.get(tag_name).run(g.db.conn)
                data = dict(data) if data else {}
            else:
                data = rdb.pluck('tag_name').run(g.db.conn)
                data = list(data) if data else []
        else:
            return self.error(ErrorCodes.invalid_api_key)

        return jsonify(data)

    def post(self):
        """ Indata must be provided as JSON. """
        rdb = rethinkdb.table(self.table)
        indata = request.get_json()
        tag_name = indata.get('tag_name')
        tag_content = indata.get('tag_content')
        tag_category = indata.get('tag_category')
        api_key = indata.get('api_key')

        if self.validate_key(api_key):
            if tag_name and tag_content:
                rdb.insert({
                    'tag_name': tag_name,
                    'tag_content': tag_content,
                    'tag_category': tag_category
                }).run(g.db.conn)
            else:
                return self.error(ErrorCodes.missing_parameters)
        else:
            return self.error(ErrorCodes.invalid_api_key)

        return jsonify({'success': True})
