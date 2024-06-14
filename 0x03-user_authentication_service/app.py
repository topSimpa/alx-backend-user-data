#!/usr/bin/env python3
"""
    Main flask app module file
"""

from auth import Auth
from flask import (
    Flask,
    jsonify,
    request
)

from flask.wrappers import Response


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> Response:
    """view function:
        response for the domain root
    """

    return jsonify({
        "message": "Bienvenue"
    })


@app.route("/users", methods=["POST"])
def users() -> Response:
    """help register a non-existing user"""

    email = request.form["email"]
    password = request.form["password"]
    try:
        new_user = Auth().register_user(email, password)
        return jsonify({
            "email": email, "message": "user created"
        })
    except ValueError as e:
        response = jsonify({
            "message": "email already registered"
        })
        response.status_code = 400
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
