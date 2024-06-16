#!/usr/bin/env python3
"""
    Main flask app module file
"""

from auth import Auth
from flask import (
    abort,
    Flask,
    jsonify,
    redirect,
    request,
)

from flask.wrappers import Response


app = Flask(__name__)
AUTH = Auth()


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
        new_user = AUTH.register_user(email, password)
        return jsonify({
            "email": email, "message": "user created"
        })
    except ValueError as e:
        response = jsonify({
            "message": "email already registered"
        })
        response.status_code = 400
        return (response)


@app.route("/sessions", methods=["POST"])
def login() -> Response:
    """logs a user in"""

    email = request.form["email"]
    password = request.form["password"]

    if not AUTH.valid_login(email, password):
        abort(401)

    new_sess_id = AUTH.create_session(email)
    response = jsonify({
        "email": email,
        "message": "logged in"
    })
    response.set_cookie("session_id", new_sess_id)

    return (response)


@app.route("/sessions", methods=["DELETE"])
def logout() -> Response:
    """logs out a user"""

    session_id = request.cookies.get("session_id")
    pos_user = AUTH.get_user_from_session_id(session_id)

    if pos_user is None:
        abort(403)
    AUTH.destroy_session(pos_user.id)
    return redirect("/", 302)


@app.route("/profile", methods=["GET"])
def profile() -> Response:
    """returns the email corresponding to user-profile"""

    session_id = request.cookies.get("session_id")
    pos_user = AUTH.get_user_from_session_id(session_id)

    if pos_user is None:
        abort(403)
    return jsonify({"email": pos_user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> Response:
    """get token for resetting password"""

    email = request.form["email"]
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password() -> Response:
    """helps to update password on the server"""

    email = request.form["email"]
    token = request.form["reset_token"]
    passwd = request.form["new_password"]

    try:
        AUTH.update_password(token, passwd)
        return jsonify({
            "email": email,
            "message": "Password updated"
        })
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
