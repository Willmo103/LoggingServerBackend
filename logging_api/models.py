from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
import datetime

Base = declarative_base()


def create_log_model(app_name):
    class LogEntry(Base):
        __tablename__ = f"log_{app_name}"
        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.datetime.utcnow)
        message = Column(Text)
        # Other fields as needed

    return LogEntry


class APIKey(Base):
    __tablename__ = "api_keys"
    key = Column(String(64), primary_key=True)
    app_name = Column(String(50), nullable=False)
    # Additional fields like creation_date, etc.
