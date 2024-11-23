#!/usr/bin/env python3
""" Session Authentication Expiration Module
"""

from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Defines the Session Auth Expiration
    """

    def __init__(self):
        """ Initialization of every SessionExpAuth object
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION', default=0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """ Creates a sessions
        Return:
            - None: if session is not created
            - session_id: if session  is created
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id, "created_at": datetime.now()}
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ find user_id by searchin with session_id
        Return:
            - None: if timeout or session_id doesn't exist
            - user_id: user that owns session_id
        """
        if session_id:
            session_dict = self.user_id_by_session_id.get(session_id)
            if session_dict:
                duration = self.session_duration
                if duration > 0:
                    if not session_dict.get('created_at'):
                        return None
                    if (session_dict['created_at'] +
                            timedelta(seconds=duration)) < datetime.now():
                        return None
                return session_dict.get('user_id')
