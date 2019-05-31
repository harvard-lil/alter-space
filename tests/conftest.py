from tests.fixtures import *
from backend import create_app
from backend.views import backend_app


@pytest.fixture
def app():
    alterspace_app = create_app()
    alterspace_app.register_blueprint(backend_app)

    return alterspace_app
