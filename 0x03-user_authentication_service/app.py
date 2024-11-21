#!/usr/bin/env python3
""" Flask Application Module
"""

from auth import Auth

from flask import Flask, jsonify, request

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def root():
    """ GET /
    Return:
       - JSON: contain "message": "Bienvenue"
    Body:
       - message: Bienvenue
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'])
def register() -> str:
    """ POST /users
    Return:
        - JSON: containing email and a sucess message, 200
        - JSON; if user already exist, returns a failure message, 400
    Body:
        - email (only on sucess): <registered email>
        - message (on sucess): user created
                  (on failure): email already registered
    """
    email = request.form['email']
    password = request.form['password']

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(email),
                       "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
