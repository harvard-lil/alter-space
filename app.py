import os
from flask import Flask

from config import config
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile(os.path.join(config.DIR, 'config/config.py'))


@app.route("/")
def hello():
    return "Hello World!"
