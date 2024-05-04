"""
This module contains the LogEntry model class.

Classes:
    LogEntry: A class used to represent a log entry.

    Methods defined here:

    __repr__(self)
        Return a string representation of the LogEntry instance.

        Returns:
            str: A string representation of the LogEntry instance.


create_log_model(app_name)
    Create a LogEntry model class for a specific application.

    Args:
        app_name (str): The name of the application.

    Returns:
        class: A LogEntry model class for the specified application.

"""
from . import Base
from sqlalchemy import Column, Integer, DateTime, Text
import datetime


def create_log_model(app_name):
    class LogEntry(Base):
        __tablename__ = f"log_{app_name}"
        id = Column(Integer, primary_key=True)
        timestamp = Column(
            DateTime,
            default=datetime.datetime.now,
            timezone=datetime.timezone.utc
        )
        message = Column(Text)

        def __repr__(self):
            return (f"<LogEntry(id={self.id}, timestamp={self.timestamp}, message='{self.message}')>")  # noqa

    return LogEntry
