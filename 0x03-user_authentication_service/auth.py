#!/usr/bin/env python3
""" Module for Authentication
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """ salts password
    Return:
        -bytes: return the salted bytes of the password
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, salt=bcrypt.gensalt())
