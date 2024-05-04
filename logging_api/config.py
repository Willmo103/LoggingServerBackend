import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "sqlite:///instance/logging_api.db")
SQLALCHEMY_DATABASE_URI = DATABASE_URL
