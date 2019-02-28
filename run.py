import os
from backend import create_app
from config import config


if __name__ == "__main__":
    app = create_app()
    app.run(host=config.ALTERSPACE_IP, threaded=True)

