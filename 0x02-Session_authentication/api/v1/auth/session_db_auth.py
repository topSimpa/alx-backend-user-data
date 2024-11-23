#!/usr/bin/env python3
""" SessionDBAuth Module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session Authentication with DB and Expiration class
    """

    def create_session(self, user_id=None) -> str:
        """ create a session that is session_id is store as
        UserSession object
        Return:
            - None if session creation fails
            - str: session_id if creation is success
        """
        session_id = super().create_session(user_id)
        if session_id:
            UserSession(user_id=user_id, session_id=session_id).save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ get user_id by requesting UserSession in the database
        based on the session_id
        Return:
           - None: if no match
           - str: user_id if match  is success
        """
        users = UserSession.search({session_id=session_id})
        if users:
            return users[0].user_id

    def destroy_session(self, request=None) -> None:
        """Destroy the userSession
        Return:
             - None
        """
        users = UserSession.search({session_id=session_id})
        if users:
            del users[0]
