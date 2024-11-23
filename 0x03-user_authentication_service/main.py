#!/usr/bin/env python3
""" Main file for testing
"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """test user registration endpoint
       POST /users
    """
    r = requests.post(
        URL + "/users",
        data={
            "email": email,
            "password": password})
    dict = r.json()
    assert dict.get("email") == email
    assert dict.get("message") == "user created"
    assert r.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """ test for failed login endpoint response
        POST /session wrong password
    """
    r = requests.post(
        URL + "/sessions",
        data={
            "email": email,
            "password": password})
    assert r.reason == "UNAUTHORIZED"
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ test sucessful login
        POST /session
    """
    r = requests.post(
        URL + "/sessions",
        data={
            "email": email,
            "password": password})
    dict = r.json()
    assert dict.get("email") == email
    assert dict.get("message") == "logged in"
    assert r.status_code == 200
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """ test profile
        GET /profile no session_id
    """
    r = requests.get(URL + "/profile")
    assert r.status_code == 403
    assert r.reason == "FORBIDDEN"


def profile_logged(session_id: str) -> None:
    """ test profile
        GET /profile session_id
    """
    r = requests.get(URL + "/profile", cookies={"session_id": session_id})
    dict = r.json()
    assert dict.get("email") is not None
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """ test DELETE /session_id
    """
    r = requests.delete(
        URL + "/sessions",
        cookies={
            "session_id": session_id},
        allow_redirects=False)
    assert r.status_code == 302


def reset_password_token(email: str) -> str:
    """ test POST /reset_password
    """
    r = requests.post(URL + "/reset_password", data={"email": email})
    assert r.status_code == 200
    dict = r.json()
    assert dict.get('email') == email
    assert dict.get('reset_token') is not None
    return dict.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test PUT /reset_password
    """
    r = requests.put(
        URL + "/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password})
    assert r.status_code == 200
    dict = r.json()
    assert dict.get('email') == email
    assert dict.get("message") == "Password updated"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
