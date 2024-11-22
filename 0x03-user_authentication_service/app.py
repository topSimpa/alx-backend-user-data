#!/usr/bin/env python3
""" Flask Application Module
"""

from auth import Auth

from flask import abort, Flask, jsonify, request, redirect, url_for

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
        - JSON: if user already exist, returns a failure message, 400
    Body:
        - email (only on sucess): <registered email>
        - message (on sucess): user created
                  (on failure): email already registered
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(email),
                       "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """ POST /sessions
    Return:
        - JSON: containing email and sucess message,
    Body:
        - email (only on sucess): <user email>
        - message (only on sucess): logged in
    Error:
         401 using flask abort
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify(
            {"email": "{}".format(email), "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response, 200
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ DELETE /sessions
    Return: redirect response
    """
    session_id = request.cookie.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    AUTH.destroy_session(user.id)
    if not user:
        abort(403)
    redirect(url_for('root'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
