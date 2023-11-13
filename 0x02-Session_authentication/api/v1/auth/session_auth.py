#!/usr/bin/env python3
"""Defines a class SessionAuth that inherits from Auth.
"""


from api.v1.auth.auth import Auth
import uuid
from api.v1.views.users import User
from api.v1.views.session_auth import *


class SessionAuth(Auth):
    """Authentication mechanism
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """An overload that returns a User instance based on a cookie value
        """
        if request is None:
            return None
        session_cookie_value = self.session_cookie(request)
        if session_cookie_value is None:
            return None

        user_id = self.user_id_for_session_id(session_cookie_value)

        if user_id is None:
            return None
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Deletes the user session / logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
