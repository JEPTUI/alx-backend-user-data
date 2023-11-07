#!/usr/bin/env python3
"""Defines the class BasicAuth
"""


from api.v1.auth.auth import Auth
import base64
import binascii


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_value = base64.b64decode(
                    base64_authorization_header).decode('utf-8')
            return decoded_value
        except (binascii.Error, UnicodeDecodeError):
            return None
