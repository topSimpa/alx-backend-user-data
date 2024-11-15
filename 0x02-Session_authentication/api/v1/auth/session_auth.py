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
        """Creates a session id for a user_id
        Return:
            - None: if user_id is None
                    if user_id is not a string
            - str: the session_id generated
        """
        if user_id:
            if isinstance(user_id, str):
                session_id = uuid4()
                self.user_id_by_session_id[session_id] = user_id
                return session_id
