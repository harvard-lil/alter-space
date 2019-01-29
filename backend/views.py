import os
import json
import requests
from flask import jsonify
from flask import request, render_template, send_from_directory
from flask import Blueprint
from config import config

from helpers import get_sound_paths

backend_app = Blueprint('backend', __name__)


@backend_app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@backend_app.route("/lights")
def lights():
    color_string = request.args.get('color_string', None)
    hex_color = "#ff0000"
    result = {
        "color_string": color_string,
        "color": hex_color
    }

    print(hex_color, request.args)
    headers = {"Authorization": "Bearer %s" % config.LIGHTS_TOKEN}
    data = {
        "power": "off",
        "fast": "true"
    }
    # url = "https://api.lifx.com/v1/lights/%s/state" % config.LIGHTS_ID
    # requests.put(url, data=data, headers=headers)
    return jsonify(result)


#
# @backend_app.route("/colorpresets")
# def getcolorpresets():


@backend_app.route("/breathe")
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


@backend_app.route("/sounds")
def sounds():
    sound_paths = get_sound_paths()
    return jsonify(sound_paths)


@backend_app.route("/sounds/<sound_id>")
def sound(sound_id):
    sound_dir = os.path.join(app.template_folder, "sounds")
    return send_from_directory(sound_dir, sound_id)


@backend_app.route("/activities")
def activities():
    return jsonify(config.ACTIVITIES)


@backend_app.route("/activity/<activity>")
def get_activity_presets(activity):
    presets = {
        "sound": config.SOUND_PRESETS[activity],
        "light": config.LIGHT_PRESETS[activity],
    }
    return jsonify(presets)


# LIFX LIGHTS

@backend_app.route("/lifx/scenes")
def list_scenes():
    headers = {"Authorization": "Bearer %s" % config.LIGHTS_TOKEN}
    results = requests.get("https://api.lifx.com/v1/scenes", headers=headers)
    return jsonify(results.json())

@backend_app.route("/lifx/relax")
def create_lights():
    headers = {"Authorization": "Bearer %s" % config.LIGHTS_TOKEN}
    data = {
        "power": "on",
        "states": [
            {
                "selector": "id:d073d52cd4cb|0-7",
                "brightness": 0.65,
                "hue": 35,
                "saturation": 0.37,
                "kelvin": 3500,
                # "duration": 600
            },
            {
                "selector": "id:d073d52cd4cb|8-15",
                "brightness": 0.9,
                "hue": 300,
                "kelvin": 3500,
            }
        ],
    }

    results = requests.put("https://api.lifx.com/v1/lights/states", data=json.dumps(data), headers=headers)
    return jsonify(results.json())
