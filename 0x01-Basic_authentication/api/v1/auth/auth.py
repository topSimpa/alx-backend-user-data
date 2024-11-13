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
        """Validates if a path should be authenticated
        Return:
           - False: if path is in excluded_paths
           - True: if path is None or not in excluded_path
           - True: if excluded path is empty or None
        """
        if path and excluded_paths:
            for x_path in excluded_paths:
                if path in x_path:
                    return False
        return True

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
