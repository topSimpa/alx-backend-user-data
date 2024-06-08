#!/usr/bin/env python3
"""
    Module for password security
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """hashes password in salted format"""

    hash_password = bcrypt.hashpw(password.encode('ascii'),
                                  bcrypt.gensalt())
    return (hash_password)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if password matches"""
    return (bcrypt.checkpw(password.encode('ascii'),
            hashed_password))
