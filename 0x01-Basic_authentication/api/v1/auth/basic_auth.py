#!/usr/bin/env python3
"""Defines the class BasicAuth
"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Inherits from Auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        base64_part = authorization_header[len('Basic '):].strip()
        return base64_part
