import secrets
from flask import jsonify
from .models import create_log_model, db_session, APIKey
import json
import click
import os
import requests as req


class Web:
    def __init__(self):
        conf = load_config()
        self.api_key = conf["api_key"]
        self.headers = {"API-Key": self.api_key}
        self.api_url = conf["api_url"]

    def get_logs(self, app_name):
        if not self.validate_api_key(self.api_key, app_name):
            return {"error": "Invalid or missing API key"}, 401

        r = req.get(f"{self.api_url}/logs/{app_name}", headers=self.headers)
        return r.json(), r.status_code

    def log(self, app_name, data):
        if not self.validate_api_key(self.api_key, app_name):
            return {"error": "Invalid or missing API key"}, 401

        r = req.post(f"{self.api_url}/log/{app_name}",
                     headers=self.headers, json=data)
        return r.json(), r.status_code

    def register_app(self, app_name):
        if not app_name:
            return {"error": "App name is required"}, 400

        r = req.post(f"{self.api_url}/register_app",
                     json={"app_name": app_name})
        return r.json(), r.status_code


class Local:
    def __init__(self):
        conf = load_config()
        self.api_key = conf["api_key"]
        self.headers = {"API-Key": self.api_key}
        self.database_path = conf["database_path"]

    def get_logs(self, app_name):
        if not self.validate_api_key(self.api_key, app_name):
            return {"error": "Invalid or missing API key"}, 401

        LogModel = create_log_model(app_name)
        logs = db_session.query(LogModel).all()
        return jsonify([log.to_dict() for log in logs]), 200

    def log(self, app_name, data):
        if not self.validate_api_key(self.api_key, app_name):
            return {"error": "Invalid or missing API key"}, 401

        LogModel = create_log_model(app_name)
        log_entry = LogModel(**data)
        db_session.add(log_entry)
        db_session.commit()
        return jsonify({"message": "Log entry added"}), 201

    def register_app(self, app_name):
        # Check if the app name is already registered
        api_key_entry = db_session.query(
            APIKey).filter_by(app_name=app_name).first()
        if api_key_entry:
            return {
                "error": "App name already registered."
            }, 400

        # Generate a new API key
        api_key = secrets.token_hex(32)
        new_api_key = APIKey(key=api_key, app_name=app_name)

        db_session.add(new_api_key)
        db_session.commit()

        # Create the log table for the app
        LogModel = create_log_model(app_name)
        LogModel.__table__.create(bind=db_session.get_bind(), checkfirst=True)

        return {"api_key": api_key}, 201

    def validate_api_key(self, api_key, app_name):
        api_key_entry = db_session.query(APIKey).filter_by(key=api_key).first()
        if api_key_entry and api_key_entry.app_name == app_name:
            return True
        return False


def load_config():
    """Loads the configuration from litelog.json."""
    if not os.path.exists("litelog.json"):
        click.echo(
            "No configuration found. Please run 'logging-api init' first.",
            err=True
        )
        raise click.Abort()

    with open("litelog.json", "r") as f:
        return json.load(f)
