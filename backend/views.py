import os
import json
import requests
from flask import jsonify
from flask import request, render_template, send_from_directory
from flask import Blueprint
from config import config, light_presets, sound_presets

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
    nature_paths = get_sound_paths('nature')
    urban_paths = get_sound_paths('urban')
    abstract_paths = get_sound_paths('abstract')
    return jsonify({
        "nature": nature_paths,
        "urban": urban_paths,
        "abstract": abstract_paths
    })

@backend_app.route("/sounds/<sound_type>")
def sounds_of_type(sound_type):
    paths = get_sound_paths(sound_type)
    return jsonify(paths)


@backend_app.route("/activities")
def activities():
    return jsonify(config.ACTIVITIES)


@backend_app.route("/activity/<activity>")
def get_activity_presets(activity):
    presets = {
        "sound": sound_presets.presets[activity],
        "light": light_presets.presets[activity],
    }
    return jsonify(presets)


# LIGHT CONTROLS
@backend_app.route("/lights/scenes")
def list_scenes():
    headers = {"Authorization": "Bearer %s" % config.LIGHTS_TOKEN}
    results = requests.get("https://api.lifx.com/v1/scenes", headers=headers)
    return jsonify(results.json())


@backend_app.route("/lights/states")
def create_lights():
    headers = {"Authorization": "Bearer %s" % config.LIGHTS_TOKEN}
    activity = request.args.get('activity', "focus")
    data = light_presets.presets[activity]
    # TODO: control each light through different url!!!
    results = requests.put("https://api.lifx.com/v1/lights/states", data=json.dumps(data), headers=headers)
    return jsonify(results.json())
