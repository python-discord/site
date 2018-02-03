#!/usr/bin/env python3

from flask import flask
import os

app = Flask(__name__)

app.secret_key = os.environ.get("WEBPAGE_SECRET_KEY")


@app.route("/")
def index():
    return "Hello."

if __name__ == '__main__':
    app.run(port=int(os.environ.get("WEBPAGE_PORT")), debug=False)
