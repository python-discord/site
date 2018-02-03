#!/usr/bin/env python3

# Stdlib
import os

# Snekchek
from flask import Flask

app = Flask(__name__)

app._secret_key = os.environ.get("WEBPAGE_SECRET_KEY")


@app.route("/")
def _index():
    return "Robots are taking over"


if __name__ == '__main__':
    app.run(port=int(os.environ.get("WEBPAGE_PORT")), debug=False)
