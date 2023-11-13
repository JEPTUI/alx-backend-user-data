#!/usr/bin/env python3
"""Defines a new authentication system, based on Session ID stored in database
"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models.base import Base
import os


class SessionDBAuth(SessionExpAuth):
    """New authenitication class
    """

    def __init__(self):
        """Initializes the class
        """
        super().__init__()

    def create_session(self, user_id=None):
        """Creates and stores new instance of UserSession
        and returns the Session ID
        """
        # Call the create_session method of SessionExpAuth
        session_id = super().create_session(user_id)

        if session_id is not None:
            # Create a new UserSession instance and add it to the database
            new_session = UserSession(user_id=user_id, session_id=session_id)
            self._db_add_instance(new_session)

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Rturns the User ID by requesting UserSession
        in the database based on session_id
        """
        if session_id is None:
            return None

        # Query the UserSession in the database based on session_id
        session = self._db_session().query(
                UserSession).filter_by(session_id=session_id).first()

        if session is None:
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID
        from the request cookie
        """
        if request is None:
            return False

        # Use self.session_cookie to get the session ID from the request
        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        # Query the UserSession in the database based on session_id
        session = self._db_session().query(
                UserSession).filter_by(session_id=session_id).first()

        if session is None:
            return False

        # Delete the session from the database
        self._db_session().delete(session)

        return True

    def _db_add_instance(self, instance):
        """Creates an instance
        """
        engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///'))
        Base.metadata.create_all(engine)
        session = Session(engine)
        session.add(instance)
        session.commit()

    def _db_session(self):
        """Creates a session
        """
        engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///'))
        Base.metadata.create_all(engine)
        return Session(engine)
