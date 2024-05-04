# tests/test_database.py
import sys
import os
from logging_api.database import db_session

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_database_connection(app):
    with app.app_context():
        result = db_session.execute("SELECT 1").scalar()
        assert result == 1
