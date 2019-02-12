import os
import logging

from flask import Flask
from flask_cors import CORS

from backend.views import backend_app
from backend import tasks

from config import config

logger = logging.getLogger()


def configure_celery(app, celery):
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # run finalize to process decorated tasks
    celery.finalize()


def configure_app(app):
    logger.info('configuring flask app')
    app.config.from_pyfile(os.path.join(config.DIR, 'config/config.py'))


def create_app():
    template_folder = os.path.join(config.DIR, "dist")
    app = Flask(__name__,
                static_url_path='/static',
                static_folder=os.path.join(template_folder, "static"),
                template_folder=template_folder)

    configure_app(app)
    configure_celery(app, tasks.celery)

    app.register_blueprint(backend_app)

    CORS(app)
    return app