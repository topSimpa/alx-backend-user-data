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
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('root'))


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ GET /profile
    Return:
        - JSON: containing sucess message
    Body:
        - email: <user email>
    Error
        - 403: if session_id is not valid
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=["POST"])
def get_reset_password_token() -> str:
    """ POST /reset_password
    Return:
        - JSON: containing sucess message
    Body:
        - email: <user email>
        - reset_token: <reset token>
    Error:
        - 403: if email is not registered
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=["PUT"])
def update_password() -> str:
    """ PUT /reset_password
    Return:
        - JSON: containing sucess message
    Body:
        - email: <user email>
        - message: Password updated
    Error:
        - 403: if token is invalid
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
