import os
import requests
from flask import Flask, jsonify
from flask import request, render_template, send_from_directory
from flask_cors import CORS

from config import config
from color.trained import get_color

from utils import get_sound_paths

app = Flask(__name__,
            static_url_path='/static',
            static_folder="./dist/static",
            template_folder="./dist")
app.config.from_pyfile(os.path.join(config.DIR, 'config/config.py'))
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/lights")
def lights():
    color_string = request.args.get('color_string', None)
    hex_color = get_color(color_string)['hex']
    result = {
        "color_string": color_string,
        "color": hex_color
    }

    print(hex_color, request.args)
    headers = {"Authorization": "Bearer %s" % config.LIGHTS_TOKEN}
    data = {
        "power": "off",
        # "color": hex_color,
        # "brightness": ,
        "fast": "true"
    }
    # url = "https://api.lifx.com/v1/lights/%s/state" % config.LIGHTS_ID
    # requests.put(url, data=data, headers=headers)
    return jsonify(result)


@app.route("/breathe")
def breathe():
    headers = {"Authorization": "Bearer %s" % config.LIGHTS_TOKEN}
    data = {
        "power_on": "true",
        "brightness": 0.2,
        "color": "#ffc1c1",
        "from_color": "#ffe0c1",
        "cycles": 8,
        "persist": "true",
        "period": 2,
        "peak": 0.5
    }
    url = "https://api.lifx.com/v1/lights/%s/effects/breathe" % config.LIGHTS_ID
    resp = requests.post(url, data=data, headers=headers)
    return jsonify(resp.status_code)


@app.route("/sounds", methods=['GET'])
def sounds():
    sound_paths = get_sound_paths()
    return jsonify(sound_paths)


@app.route("/sounds/<sound_id>", methods=['GET'])
def sound(sound_id):
    sound_dir = os.path.join(app.template_folder, "sounds")
    return send_from_directory(sound_dir, sound_id)


@app.route("/activities")
def activities():
    return jsonify(config.ACTIVITIES)
