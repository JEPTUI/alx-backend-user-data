#!/usr/bin/env python3
"""Defines a class SessionExpAuth that inherits from SessionAuth
"""


from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Adds expiration date to session ID
    """
    def __init__(self):
        """Initializes the class SessionExpAuth
        """
        super().__init__()

        # Assign session_duration attribute from environment variable
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Calls the create_session method of SessionAuth
        """
        session_id = super().create_session(user_id)

        if session_id is not None:
            # Create a session dictionary
            session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()
            }

            # Use the Session ID as the key in the dictionary
            self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload
        """
        if session_id is None:
            return None

        # Check if the session dictionary contains the session_id
        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None

        user_id = session_dict.get('user_id')

        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get('created_at')

        if created_at is None or (
                created_at + timedelta(
                    seconds=self.session_duration)) < datetime.now():
            return None

        return user_id
