#!/usr/bin/env python3
""" Flask Application Module
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    """ GET /
    Return:
       - JSON: contain "message": "Bienvenue"
    Body:
       - message: Bienvenue
    """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
