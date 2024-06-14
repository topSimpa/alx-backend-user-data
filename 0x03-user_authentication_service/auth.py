#!/usr/bin/env python3
"""
    Module for authentications
"""

import bcrypt
from db import (
    DB,
    NoResultFound
)

from user import User


def _hash_password(password: str) -> bytes:
    """hashes a password"""
    pw_byte = password.encode("ascii")
    hash_password = bcrypt.hashpw(pw_byte, bcrypt.gensalt())
    return (hash_password)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user if the user does not previously exist"""
        try:
            user_check = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            h_passwd = _hash_password(password)
            n_user = self._db.add_user(email, h_passwd)
            return (n_user)

    def valid_login(self, email: str, password: str) -> bool:
        """check if login details are correct"""

        try:
            pot_user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(
                                          'ascii'), pot_user.hashed_password)
        except Exception:
            return False
