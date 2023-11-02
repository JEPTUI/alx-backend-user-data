#!/usr/bin/env python3
"""Defines a function that implements a
hash password"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Uses bycrypt to return a  a salted, hashed password
    which is a byte string"""
    encoded_pw = password.encode()
    hashed_pw = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())

    return hashed_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password"""
    valid = False
    encoded_pw = password.encode()
    if bcrypt.checkpw(encoded_pw, hashed_password):
        valid = True
    return valid
