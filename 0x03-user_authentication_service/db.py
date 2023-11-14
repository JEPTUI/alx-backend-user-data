#!/usr/bin/env python3
"""Defines DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm.exc import MultipleResultsFound
from user import User
from user import Base


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
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound(
                        "No user found with the specified criteria")
            return user
        except NoResultFound:
            raise
        except InvalidRequestError as e:
            self._session.rollback()
            if "No user found" in str(e):
                raise NoResultFound(
                        "No user found with the specified criteria") from e
            else:
                raise InvalidRequestError(f"Invalid query arguments: {str(e)}")
        finally:
            self._session.close()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes in the database

        Args:
            user_id (int): ID of the user to update
            **kwargs: Arbitrary keyword arguments for updating user attributes

        Raises:
            ValueError: If an invalid argument is passed
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid argument: {key}")
            self._session.commit()
        except NoResultFound:
            print("User not found")
            raise
        except MultipleResultsFound:
            print("Multiple users found with the same ID")
            raise
        finally:
            self._session.close()
