import os
from flask import Flask
from flask_cors import CORS
from backend.views import backend_app
from config import config


def create_app():
    app = Flask(__name__,
                static_url_path='/static',
                static_folder="../dist/static",
                template_folder="../dist")
    app.register_blueprint(backend_app)
    app.config.from_pyfile(os.path.join(config.DIR, 'config/config.py'))
    CORS(app)
    return app
