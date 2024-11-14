#!/usr/bin/env python3
""" Module for Basic_auth implementation
"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode the bas64 part of the authorization header
        Return:
            - None: if base64_authorization_header is None
                    if base64_authorization_header is not a string
                    if base64_authorization_header is not a valid base64
            - str: value of decoded base64 key
        """
        if base64_authorization_header:
            if isinstance(base64_authorization_header, str):
                try:
                    return base64.b64decode(
                        base64_authorization_header).decode('utf-8')
                except BaseException:
                    pass

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract user credentials email and password from decoded_b64_header
        Return:
            - None: if decoded_base64_authorization_header is None
                    if decoded_base64_authorization_header is not a string
                    if decoded_base64_authorization_header doesn't contain :
            - (str, str): A tuple of email and password

        """
        if decoded_base64_authorization_header:
            if isinstance(decoded_base64_authorization_header, str):
                if ':' in decoded_base64_authorization_header:
                    return tuple(
                        decoded_base64_authorization_header.split(':'))
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """return a user with that email and password
        Return:
            - None: if user_email is None is None or not a string
                    if user_pwd is None or not a string
                    if database don't have that user_email
                    if user_pwd is not correct
            - User: the user with the corresponding credentials
        """
        if user_email and user_pwd:
            if isinstance(user_email, str) and isinstance(user_pwd, str):
                users = User.search({'email': user_email})
                if users:
                    for user in users:
                        if user.is_valid_password(user_pwd):
                            return user
