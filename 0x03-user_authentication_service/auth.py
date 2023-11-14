#!/usr/bin/env python3
"""auth module
"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes auth class
        """
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash the input password using bcrypt.hashpw
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """Register a new user and return the User object
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(
                    email=email, hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login credentials are valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Generate and return a string representation of a new UUID
        """
        new_uuid = uuid.uuid4()
        return str(new_uuid)

    def create_session(self, email: str) -> str:
        """Create a new session for the user and return the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user corresponding to the session ID or None if not found
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Update the user's session ID to None
        """
        self._db.update_user(user_id, session_id=None)
