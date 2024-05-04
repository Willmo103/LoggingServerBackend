# routes/auth.py
import secrets
from flask import Blueprint, request, jsonify
from logging_api.models.api_key import APIKey
from logging_api.models.log_entry import create_log_model
from logging_api.database import db_session

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register_app", methods=["POST"])
def register_app():
    app_name = request.json.get("app_name")
    if not app_name:
        return jsonify({"error": "App name is required"}), 400

    api_key = secrets.token_hex(32)
    new_api_key = APIKey(key=api_key, app_name=app_name)
    db_session.add(new_api_key)
    db_session.commit()

    LogModel = create_log_model(app_name)
    LogModel.__table__.create(bind=db_session.get_bind(), checkfirst=True)

    return jsonify({"api_key": api_key}), 201
