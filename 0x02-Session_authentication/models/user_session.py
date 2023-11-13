#!/usr/bin/env python3
"""Defines a new model that inherits from Base
"""


from sqlalchemy import Column, String, ForeignKey
from models.base import Base
from sqlalchemy import Column, String, ForeignKey


class UserSession(Base):
    """Inherits from base
    """
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(60), nullable=False)

    def __init__(self, *args: list, **kwargs: dict):
        """initializes the class
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', '')
