import os
from flask import Flask

from config import config
from flask import request, render_template

from color.trained import get_color

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile(os.path.join(config.DIR, 'config/config.py'))


@app.route("/")
def hello():
    return render_template("main.html")


@app.route("/lights", methods=['GET', 'POST'])
def lights():
    if request.method == 'GET':
        return render_template("lights.html")
    elif request.method == 'POST':
        color_string = request.form.get('color', None)

        if not color_string:
            return render_template("lights.html")

        hex_color = get_color(color_string)['hex']
        return render_template("lights.html", color_string=color_string, color=hex_color)
