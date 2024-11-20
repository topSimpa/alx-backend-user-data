#!/usr/bin/env python3
""" Module for Authentication
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar

from db import DB


def _hash_password(password: str) -> bytes:
    """ salts password
    Return:
        -bytes: return the salted bytes of the password
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, salt=bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ create a user and save it in the database
        Return:
            - User: user that was created
        Error:
            - ValueError: when user email already exist

        """
        hash_password = _hash_password(password)
        try:
            exist = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            return self._db.add_user(email, hash_password)
