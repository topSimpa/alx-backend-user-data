#!/usr/bin/env python3
""" Views that handles all routes
 for the Session authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """	POST /api/v1/auth_session/login
    Return:
        - {error: email missing} 400: if email is missing or empty
        - {error: passwordmissing} 400: if password is missing
        - {error: no user found} 404: if no User found
        - {error: wrong password} 401: if password mismatch
        - User object in json format if successful
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except BaseException:
        return jsonify({"error": "no user found"}), 404
    if not users:
        return jsonify({"error": "no user found for this user email"}), 404
    for user in users:
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            response = jsonify(user.to_json)
            response.set_cookie(
                getenv('SESSION_NAME'),
                auth.create_session(
                    user.id))
            return response, 200
    return jsonify({"error": "wrong password"})
