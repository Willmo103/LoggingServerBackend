from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base
from . import config

engine = create_engine(config.DATABASE_URL)
db_session = scoped_session(sessionmaker(bind=engine))


def init_db():
    Base.metadata.create_all(bind=engine)
