"""
This module contains the APIKey model.

Classes:
    APIKey: A class used to represent an API key.


APIKey(Base)
---> __tablename__ = "api_keys"
---> key = Column(String(64), primary_key=True)
---> app_name = Column(String(50), nullable=False)

    Methods defined here:

    __repr__(self)
        Return a string representation of the APIKey instance.

        Returns:
            str: A string representation of the APIKey instance.
"""

from . import Base
from sqlalchemy import Column, String


class APIKey(Base):
    __tablename__ = "api_keys"
    key = Column(String(64), primary_key=True)
    app_name = Column(String(50), nullable=False)

    def __repr__(self):
        return (
            f"<APIKey(key='{self.key}', app_name='{self.app_name}')>"
        )
