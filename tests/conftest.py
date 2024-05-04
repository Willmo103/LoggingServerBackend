# tests/conftest.py
from logging_api.database import db_session, init_db
from logging_api import create_app
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    init_db()
    yield app
    db_session.remove()
    db_session.close()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
