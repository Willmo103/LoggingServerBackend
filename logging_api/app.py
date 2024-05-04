# from flask import Blueprint, request, jsonify
# from .models import create_log_model, APIKey
# from .database import db_session
# from .controllers import validate_api_key
# import secrets
# from .controllers import Web

# # Create the API blueprint
# api_bp = Blueprint("api_bp", __name__)

# # init the controller
# DB = Web()


# @api_bp.route("/log/<app_name>", methods=["POST"])
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


# @api_bp.route("/register_app", methods=["POST"])
# def register_app():
#     app_name = request.json.get("app_name")
#     if not app_name:
#         return jsonify({"error": "App name is required"}), 400

#     api_key = secrets.token_hex(32)
#     new_api_key = APIKey(key=api_key, app_name=app_name)
#     db_session.add(new_api_key)
#     db_session.commit()

#     LogModel = create_log_model(app_name)
#     LogModel.__table__.create(bind=db_session.get_bind(), checkfirst=True)

#     return jsonify({"api_key": api_key}), 201
