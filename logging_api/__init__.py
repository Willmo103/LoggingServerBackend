from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('instance/config.py')
    
    init_db(app)

    from .app import api_bp
    app.register_blueprint(api_bp)

    return app

