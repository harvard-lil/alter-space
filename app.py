import os
from flask import Flask, jsonify

from config import config
from flask import request, render_template, send_from_directory

from color.trained import get_color

from flask_cors import CORS

app = Flask(__name__,
            static_url_path='/static',
            static_folder="./dist/static",
            template_folder="./dist")
app.config.from_pyfile(os.path.join(config.DIR, 'config/config.py'))
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('hello from backend pong!')


@app.route("/lights")
def lights():

    color_string = request.args.get('color_string', None)
    hex_color = get_color(color_string)['hex']
    print(color_string, hex_color, request.args)
    result = {
        "color_string": color_string,
        "color": hex_color
    }
    return jsonify(result)


@app.route("/sounds", methods=['GET'])
def sounds():
    sound_paths = get_sound_paths()
    return jsonify(sound_paths)


@app.route("/sounds/<sound_id>", methods=['GET'])
def sound(sound_id):
    sound_dir = os.path.join(app.template_folder, "sounds")
    return send_from_directory(sound_dir, sound_id)
