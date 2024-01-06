from flask import Blueprint, request, jsonify
from .models import create_log_model, APIKey
from .database import db_session
import secrets

api_bp = Blueprint("api_bp", __name__)


def validate_api_key(api_key, app_name):
    api_key_entry = (
        db_session.query(APIKey).filter_by(key=api_key, app_name=app_name).first()
    )
    return api_key_entry is not None


@api_bp.route("/log/<app_name>", methods=["POST"])
def log(app_name):
    api_key = request.headers.get("API-Key")
    if not api_key or not validate_api_key(api_key, app_name):
        return jsonify({"error": "Invalid or missing API key"}), 401

    LogModel = create_log_model(app_name)
    data = request.json
    log_entry = LogModel(**data)
    db_session.add(log_entry)
    db_session.commit()
    return jsonify({"message": "Log entry added"}), 201


@api_bp.route("/logs/<app_name>", methods=["GET"])
def get_logs(app_name):
    api_key = request.headers.get("API-Key")
    if not api_key or not validate_api_key(api_key, app_name):
        return jsonify({"error": "Invalid or missing API key"}), 401

    LogModel = create_log_model(app_name)
    logs = db_session.query(LogModel).all()
    return jsonify([log.to_dict() for log in logs]), 200


@api_bp.route("/register_app", methods=["POST"])
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
