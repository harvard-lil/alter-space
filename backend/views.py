import json
import logging

import requests
from flask import jsonify, Blueprint, request, render_template, make_response
from config import config, light_presets, sound_presets

from backend import tasks


from helpers import get_sound_paths

logger = logging.getLogger()

backend_app = Blueprint('backend', __name__)
tsk = Blueprint('backend.tasks', __name__)


@tsk.route('/task/start/<task_name>', methods=['POST'])
@backend_app.route('/task/start/<task_name>', methods=['POST'])
def view_start_task(task_name):
    """start task, return task_id"""

    logger.info('start task...')
    if task_name == "wait":
        sleep_time = int(request.form.get('sleep_time', 5))
        task = tasks.wait_task.apply_async(kwargs={'sleep_time': sleep_time})
        data = {"sleep_time": sleep_time}
    elif task_name == "breathe":
        id = request.form.get('id')
        task = tasks.breathe_task.apply_async(kwargs={'id': id})
        data = {"id": id}
    elif task_name == "chase":
        id = request.form.get('id')
        task = tasks.chase_task.apply_async(kwargs={'id': id})
        data = {"id": id}
    else:
        error_message = "Task with name %s was not found" % task_name
        return make_response(error_message, 404)

    logger.info('return task...')

    return jsonify({
        'task_id': task.id,
        'state': task.state,
        'data': data}), 202


@tsk.route('/task/stop/<task_name>', methods=['POST'])
@backend_app.route('/task/stop/<task_name>', methods=['POST'])
def stop_task(task_name):
    """start task, return task_id"""

    task_id = request.form.get('task_id')
    print('stop task...', task_id)

    task = tasks.stop_task.delay(task_name, task_id)
    data = {"id": task_id}

    return jsonify({
        'task_id': task.id,
        'state': task.state,
        'data': data}), 202


@tsk.route('/task/<task_name>/<task_id>', methods=['GET'])
@backend_app.route('/task/<task_name>/<task_id>', methods=['GET'])
def view_check_task(task_name, task_id):
    """return task state"""
    if task_name == "wait":
        task = tasks.wait_task.AsyncResult(task_id)
    elif task_name == "breathe":
        task = tasks.breathe_task.AsyncResult(task_id)
    output = {'task_id': task.id, 'state': task.state}
    if task.state == 'SUCCESS':
        output.update({'result': task.result})
    return jsonify(output)


@backend_app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


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
@backend_app.route("/lights/effects/<effect_type>", methods=['POST'])
def toggle_effect(effect_type):
    effect_status = request.form.get('effect')
    effect_status = True if effect_status == "true" else False
    light_id = request.form.get('id')
    data = {"id": light_id}
    if effect_status:
        results = requests.post("http://localhost:5000/task/start/%s" % effect_type, data=data)
        return jsonify(results.json())
    else:
        data["task_id"] = request.form.get('task_id')
        results = requests.post("http://localhost:5000/task/stop/%s" % effect_type, data=data)
        return jsonify(results.json())


@backend_app.route("/lights/colors")
def get_color_presets():
    colors = light_presets.colors
    return jsonify(colors)


@backend_app.route("/lights/set", methods=['POST'])
def set_light():
    light_id = request.form.get('id')
    colors = json.loads(request.form.get('colors'))['color_data']
    dim_value = request.form.get('bright', 100)

    try:
        tasks.light_task.apply_async(kwargs={'id': light_id, 'colors': colors, 'dim_value': dim_value})
        return "ok"
    except Exception as e:
        raise Exception(e, "Something went wrong!")


@backend_app.route("/lights/dim", methods=['POST'])
def set_dim():
    light_id = request.form.get('id')
    dim_level = request.form.get('bright', 100)
    try:
        tasks.dim_task.apply_async(kwargs={'id': light_id, 'dim_value': dim_level})
        return "ok"
    except Exception as e:
        raise Exception(e, "Something went wrong!")
