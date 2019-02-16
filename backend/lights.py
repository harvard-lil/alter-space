import os
import shutil
from time import sleep
from random import randint

import pickle

from lifxlan import LifxLAN
from lifxlan.errors import WorkflowException
from lifxlan.utils import RGBtoHSBK

from config import config

light_store = os.path.join(config.DIR, 'backend/lightstore')

lan = LifxLAN()


def setup_light_store():
    # Clear store before setting lights again

    if os.path.exists(light_store):
        print("removing and creating dir")
        shutil.rmtree(light_store)
        os.mkdir(light_store)


def turn_light_on(light_obj):
    power = light_obj.get_power()
    if not power:
        light_obj.set_power(True)
    return light_obj.get_power()


def get_lights():
    lights = lan.get_lights()
    return lights


def store_lights(lights, lightdir=light_store):
    for light in lights:
        store_light(light, lightdir=lightdir)
    return lights


def store_light(light_obj, lightdir=light_store):
    light_identifier = light_obj.mac_addr.replace(":", "")
    light_path = os.path.join(lightdir, light_identifier)

    with open(light_path, "wb") as f:
        pickle.dump(light_obj, f)
    return light_obj


def get_or_create_light(light_id):
    if ":" in light_id:
        # id is a mac address
        light_id = light_id.replace(":", "")
    light_path = os.path.join(light_store, light_id)
    if not os.path.exists(light_path):
        light_obj = get_light(light_id)
        store_light(light_obj)
        turn_light_on(light_obj)
        return light_obj
    else:
        with open(light_path, "rb") as f:
            light_obj = pickle.load(f)
        turn_light_on(light_obj)
        return light_obj


def get_light(id, count=0):
    all_lights = []
    while not len(all_lights):
        sleep(0.5)
        all_lights = lan.get_lights()

    mac_addr = ""
    for key, part in enumerate(id):
        if (key + 2) % 2 == 0 and key != 0:
            mac_addr += ":"
        mac_addr += part
    for light in all_lights:
        if mac_addr in light.device_characteristics_str(""):
            return light
    if count >= 4:
        raise Exception("No light found at id %s" % id)
    else:
        # wifi connection is bad? light wasn't found, try again
        get_light(id, count=count + 1)


def chase(id):
    try:
        strip = get_or_create_light(id)
        all_zones = strip.get_color_zones()
        last = all_zones.pop()
        all_zones.insert(0, last)
        strip.set_zone_colors(all_zones)
    except WorkflowException as err:
        print("caught exception", err)
        sleep(0.5)
        chase(id)


def breathe(id):
    #TODO: deep breath is 4 to inhale, 7 to hold, and 8 to exhale
    try:
        strip = get_or_create_light(id)
        all_zones = strip.get_color_zones()
        dim_zones = []
        bright_zones = []

        for [h, s, v, k] in all_zones:
            dim_zones.append((h, s, 20000, k))
            bright_zones.append((h, s, 55535, k))

        strip.set_zone_colors(bright_zones, 2000, True)
        sleep(randint(2, 10))
        strip.set_zone_colors(dim_zones, 2000, True)
        sleep(randint(2, 10))
    except WorkflowException as err:
        print("caught exception", err)
        sleep(0.5)
        breathe(id)


def set_colors(id, colors, dim_value=100):
    # TODO: transition nicely
    strip = get_or_create_light(id)
    new_zones = []
    dim_level = get_dim_value(dim_value)

    for idx, color in enumerate(colors):
        rgb = hex2rgb(color)
        h, s, v, k = RGBtoHSBK(rgb)
        new_zones.append((h, s, dim_level, k))
    try:
        strip.set_zone_colors(new_zones, 3000, False)
    except WorkflowException as err:
        print("caught exception", err)
        sleep(0.5)
        set_colors(id, colors, dim_value)


def dim(id, dim_level):
    try:
        strip = get_or_create_light(id)
        all_zones = strip.get_color_zones()
        dim_zones = []
        dim_level = get_dim_value(dim_level)
        for [h, s, v, k] in all_zones:
            dim_zones.append((h, s, dim_level, k))
        strip.set_zone_colors(dim_zones, 3000, False)
    except WorkflowException as err:
        print("caught exception", err)
        sleep(0.5)
        dim(id, dim_level)


def hex2rgb(hex):
    if hex[0] == "#":
        hex = hex.split("#")[1]
    red, green, blue = bytes.fromhex(hex)
    return red, green, blue


def get_dim_value(dim_value):
    dim_value = int(65535 * (int(dim_value) / 100))
    dim_value = 1000 if dim_value < 1000 else dim_value
    return dim_value
