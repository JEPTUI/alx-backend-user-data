#!/usr/bin/env python3
"""auth module
"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid
from db import DB
from user import User


def _hash_password(self, password: str) -> bytes:
    """Hash the input password using bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def _generate_uuid(self) -> str:
    """Generate and return a string representation of a new UUID
    """
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes auth class
        """
        self._db = DB()

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

    def get_reset_password_token(self, email: str) -> str:
        """Generate and return a reset password token for the user
        """
        user = self._db.find_user_by(email=email)

        if user:
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
        else:
            raise ValueError(f"User with email {email} does not exist.")

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password using the reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                    user.id, hashed_password=hashed_password,
                    reset_token=None)
        except NoResultFound as e:
            raise ValueError(
                    f"User with reset_token {reset_token} does not exist.")
