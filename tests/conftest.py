import pytest

from backend import create_app
from backend.views import backend_app

@pytest.fixture
def app():
    app = create_app()
    app.register_blueprint(backend_app)

    return app

