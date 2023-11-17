#!/usr/bin/env python3
"""Defines DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm.exc import MultipleResultsFound
from user import User
from user import Base

FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): User's email
            hashed_password (str): User's hashed password

        Returns:
            User: User object added to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by given filter criteria

        Args:
            **kwargs: Arbitrary keyword arguments for filtering

        Returns:
            User: User object found in the database

        Raises:
            NoResultFound: If no results are found
            InvalidRequestError: If wrong query arguments are passed
        """
        if not kwargs or any(k not in FIELDS for k in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes in the database

        Args:
            user_id (int): ID of the user to update
            **kwargs: Arbitrary keyword arguments for updating user attributes

        Raises:
            ValueError: If an invalid argument is passed
        """
        user = self.find_user_by(id=user_id)
        session = self._session
        if kwargs and any(k in FIELDS for k in kwargs):
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
        else:
            raise ValueError
