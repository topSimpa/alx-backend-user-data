#!/usr/bin/env python3
""" Module for session authentication
"""


from api.v1.auth.auth import Auth
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
