#!/usr/bin/env python3
"""Defines a class auth
"""


from flask import requests
from typing import List, TypeVar


class Auth():
    """ defines authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Manages paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Handles authentication requests
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Handles authentication users
        """
        return None
