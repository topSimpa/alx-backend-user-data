#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base
from user import User
from typing import Any, TypeVar


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """ Add and save a user to the database
        Return:
            - User: User object created
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Any) -> TypeVar('User'):
        """ Find the first user row that matches the keys and values
        Return:
            - Row: first user row retrieve
            - Raises NoResultFound and InvalidRequestError accordingly
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
        except AttributeError:
            raise InvalidRequestError
        return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """ Update the existing field of a user in the map table
        Return:
          - None
          - raise ValueError: if argument does not match user attribute

        """
        user = self.find_user_by(id=user_id)
        if not all(hasattr(user, key) for key in kwargs):
            raise ValueError
        # vars(user).update(kwargs)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()
