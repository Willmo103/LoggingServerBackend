# path: logging_api/__init__.py
from flask import Flask
from .database.database import db_session, init_db
from .routes.logs import logs_bp
from .routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("logging_api.config")

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.register_blueprint(logs_bp)
    app.register_blueprint(auth_bp)

    return app
