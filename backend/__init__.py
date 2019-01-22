import os
from flask import Flask
from flask_cors import CORS
from backend.views import backend_app
from config import config


def create_app():
    template_folder = os.path.join(config.DIR, "dist")
    app = Flask(__name__,
                static_url_path='/static',
                static_folder=os.path.join(template_folder, "static"),
                template_folder=template_folder)
    app.register_blueprint(backend_app)
    app.config.from_pyfile(os.path.join(config.DIR, 'config/config.py'))
    CORS(app)
    return app

# for deployment via uWSGI
app = create_app()
