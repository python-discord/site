#!/usr/bin/env python3

# Stdlib
import os

# Snekchek
from flask import Flask
from flask import jsonify

app = Flask(__name__)

app._secret_key = os.environ.get("WEBPAGE_SECRET_KEY")


@app.route("/")
def _index():
    return "Robots are taking over"


@app.route("/healthcheck")
def healthcheck():
    return jsonify({"status":"ok"})


@app.errorhandler(404)
def page_not_found(e):
    return "replace me with a template, 404 not found", 404


if __name__ == '__main__':
    app.run(port=int(os.environ.get("WEBPAGE_PORT")), debug=False)
