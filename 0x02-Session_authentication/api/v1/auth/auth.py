#!/usr/bin/env python3
"""Defines a class auth
"""


from flask import request
from typing import List, TypeVar
import os


class Auth():
    """ defines authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Manages paths
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if path.endswith('/'):
                path = path.rstrip('/')
            if excluded_path.endswith('/'):
                excluded_path = excluded_path.rstrip('/')
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Handles authentication requests
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Handles authentication users
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request
        """
        if request is None:
            return None
        session_cookie_name = os.getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(session_cookie_name)
