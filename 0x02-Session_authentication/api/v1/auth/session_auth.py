#!/usr/bin/env python3
""" Module for session authentication
"""


from api.v1.auth.auth import Auth
from models.user import User
from os import getenv
from typing import TypeVar
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Authentication management class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session id for a user_id
        Return:
            - None: if user_id is None
                    if user_id is not a string
            - str: the session_id generated
        """
        if user_id:
            if isinstance(user_id, str):
                session_id = str(uuid4())
                self.user_id_by_session_id[session_id] = user_id
                return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get a user_id by using the session_id
        Return:
            - None: if session_id is None
                    if session_id is not a string
            - str: the user_id which corresponds to the session_id
        """
        if session_id:
            if isinstance(session_id, str):
                return (self.user_id_by_session_id.get(session_id))

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the user based on a cookie value
        Return:
            - User: the user associated with that cookie value
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """ Deletes the user session
        Return:
            - False: if request is None
                     if no session_id cookie in request.cookie
                     if session_id is not linked to any user
            - True: if deletion is sucessful
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                user_id = self.user_id_for_session_id(session_id)
                if user_id:
                    del self.user_id_by_session_id[session_id]
                    return True
        return False
