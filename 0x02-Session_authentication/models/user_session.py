#!/usr/bin/env python3
""" User Session Module
"""

from models.base import Base


class UserSession(Base):
    """ User Session Class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initializes the UserSession object
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
