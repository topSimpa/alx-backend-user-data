#!/usr/bin/env python3
""" Module for managing API authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Implementation of the Auth class that manages the authentication
    """

    def __init__(self):
        """Object initialization of auth object"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Don't know yet
        Return:
         - False
        """
        return False

    def authorization_header(self, requests=None) -> str:
        """
        Return:
           - None
        """
        return None

    def current_user(self, requests=None) -> TypeVar('User'):
        """
        Return:
           - None
        """
        return None
