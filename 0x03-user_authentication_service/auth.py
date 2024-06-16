#!/usr/bin/env python3
"""
    Module for authentications
"""

from db import (
    DB,
    NoResultFound
)

from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """hashes a password"""
    pw_byte = password.encode("ascii")
    hash_password = bcrypt.hashpw(pw_byte, bcrypt.gensalt())
    return (hash_password)


def _generate_uuid() -> str:
    """generates a random identifier"""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """creates a new session for a user"""

        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=_generate_uuid())
            return (user.session_id)
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """get a user using its session_id"""

        if session_id is None:
            return None
        try:
            pos_user = self._b.find_user_by(session_id=session_id)
            return (pos_user)
        except Exception:
            return (None)
