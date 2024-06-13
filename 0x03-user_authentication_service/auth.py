#!/usr/bin/env python3
"""
    Module for authentications
"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """hashes a password"""
    pw_byte = password.encode("ascii")
    hash_password = bcrypt.hashpw(pw_byte, bcrypt.gensalt())
    return (hash_password)
