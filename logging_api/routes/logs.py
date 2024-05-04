# # routes/logs.py
# from flask import Blueprint, request, jsonify
# from ..models import LogEntry
# from ..database import db_session
# from logging_api.utils.helpers import validate_api_key TODO: Implement this function

# logs_bp = Blueprint("logs", __name__)


# @logs_bp.route("/log/<app_name>", methods=["POST"])
# def log(app_name):
#     # Check if the API key is valid
#     api_key = request.headers.get("API-Key")
#     if not api_key or not validate_api_key(api_key, app_name):
#         return jsonify({"error": "Invalid or missing API key"}), 401
#     return DB.log(app_name, request.json)


# @api_bp.route("/logs/<app_name>", methods=["GET"])
# def get_logs(app_name):
#     api_key = request.headers.get("API-Key")
#     if not api_key or not validate_api_key(api_key, app_name):
#         return jsonify({"error": "Invalid or missing API key"}), 401

#     LogModel = create_log_model(app_name)
#     logs = db_session.query(LogModel).all()
#     return jsonify([log.to_dict() for log in logs]), 200
