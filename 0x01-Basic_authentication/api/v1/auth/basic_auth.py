#!/usr/bin/env python3
""" Module for Basic_auth implementation
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth Authentication implementation for Api
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the base64 part of Authorization header
        Return:
          - None: if authorization_header is None
                  if authorization_header is not a string
                  if authorization_header does not start with 'Basic '
            str: value after Basic in authorization_header
        """
        if authorization_header:
            if isinstance(authorization_header, str):
                if authorization_header[:6] == 'Basic ':
                    return (authorization_header.replace('Basic ', ''))
