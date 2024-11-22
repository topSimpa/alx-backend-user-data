#!/usr/bin/env python3
""" Module for Authentication
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
import uuid

from db import DB


def _generate_uuid() -> str:
    """ generate a string representaion of a new uuid
    Return:
        - str: the str format of uuid
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """ create a new session
        Return:
            - str: the session_id generated using uuid
        """
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=_generate_uuid())
            return user.session_id
        except BaseException:
            return None

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates user login credentials
        Return:
            - True: if user credentials are correct
            - False: if user credentials are not correct
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except BaseException:
            return False

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """ fetch the user corresponding to a session_id
        Return:
            - None: if no user is found
            - User: user matching session_id
        """
        try:
            if not session_id:
                return None
            user = self._db.find_user_by(session_id=session_id)
            return user
        except BaseException:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ change the user session_id field to None
        Return
            - None: in all cases
        """
        user = self._db.find_user_by(id=user_id)
        self._db.update_user(user_id, session_id=None)
