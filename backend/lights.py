import os
import shutil
from time import sleep
from random import randint
import logging

import pickle

from lifxlan import LifxLAN
from lifxlan.errors import WorkflowException
from lifxlan.utils import RGBtoHSBK

from config import config

logger = logging.getLogger()

light_store = os.path.join(config.DIR, 'backend/lightstore')

lan = LifxLAN()

retry_count = 5


def setup_light_store():
    # Clear store before setting lights again
    logger.info("Setting up light store")

    if os.path.exists(light_store):
        logger.info("Removing and creating light store dir")
        shutil.rmtree(light_store)
    os.mkdir(light_store)


def turn_light_on(light_obj):
    power = light_obj.get_power()
    logger.info("turning light on")
    if not power:
        light_obj.set_power(True)
    return light_obj.get_power()


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
    if not light_id:
        raise Exception("No light found", light_id)
    # convert light id to actual hardware id
    light_id = config.LIGHTS[light_id]
    if ":" in light_id:
        # id is a mac address
        light_id = light_id.replace(":", "")

    light_path = os.path.join(light_store, light_id)
    if not os.path.exists(light_path):
        logger.info("Creating light %s" % light_id)
        light_obj = get_light(light_id)
        # turn light on
        store_light(light_obj)
        turn_light_on(light_obj)
        return light_obj
    else:
        with open(light_path, "rb") as f:
            light_obj = pickle.load(f)
        turn_light_on(light_obj)
        return light_obj


def get_light(light_id, count=0):
    all_lights = []
    getting_lights_count = 0
    while not (len(all_lights) and getting_lights_count < retry_count):
        logger.info("Getting all lights")
        sleep(0.5 * getting_lights_count)
        all_lights = lan.get_lights()
        logger.info("All lights: %s" % all_lights)
        getting_lights_count += 1

    mac_addr = ""
    for key, part in enumerate(light_id):
        if (key + 2) % 2 == 0 and key != 0:
            mac_addr += ":"
        mac_addr += part
    for light in all_lights:
        if mac_addr in light.device_characteristics_str(""):
            logger.info("Light was found: %s" % mac_addr)
            return light
    if count < retry_count:
        # wifi connection is bad? light wasn't found, try again
        logger.info("Light was not found. Retrying.")
        sleep(0.5 * (count + 1))
        get_light(light_id, count=count + 1)
    else:
        logger.error("No light found at id %s" % light_id)
        raise Exception("No light found at id %s" % light_id)


def chase(light_id, count=0):
    try:
        strip = get_or_create_light(light_id)
        all_zones = strip.get_color_zones()
        last = all_zones.pop()
        all_zones.insert(0, last)
        strip.set_zone_colors(all_zones, 500, False)
        sleep(0.5)
    except WorkflowException as err:
        if count < retry_count:
            sleep(0.5 * (count + 1))
            chase(light_id, count=count+1)
        else:
            logger.error("Chase: Caught exception %s" % err)


def breathe(light_id, count=0, breathe_type=None):
    if breathe_type == "relax":
        # deep breath is 4 to inhale, 7 to hold, and 8 to exhale
        bright_timer = 4000
        dim_timer = 2000
        wait_timer_1 = 7
        wait_timer_2 = 2
    else:
        bright_timer = 2000
        dim_timer = 2000
        wait_timer_1 = 2
        wait_timer_2 = 2

    try:
        strip = get_or_create_light(light_id)
        all_zones = strip.get_color_zones()
        dim_zones = []
        bright_zones = []

        for [h, s, v, k] in all_zones:
            dim_zones.append((h, s, 20000, k))
            bright_zones.append((h, s, 55535, k))
        logger.info("Brightening %s" % light_id)
        strip.set_zone_colors(bright_zones, bright_timer, True)
        sleep(wait_timer_1)
        logger.info("Dimming %s" % light_id)
        strip.set_zone_colors(dim_zones, dim_timer, True)
        sleep(wait_timer_2)
    except WorkflowException as err:
        if count < retry_count:
            sleep(0.5 * (count + 1))
            breathe(light_id, count=count+1)
        else:
            logger.error("Breathe: Caught exception %s" % err)


def set_colors(light_id, colors, dim_value=100, count=0, duration=3000):
    logger.info("set colors called")
    strip = get_or_create_light(light_id)
    new_zones = []
    dim_level = get_dim_value(dim_value)

    for idx, color in enumerate(colors):
        rgb = hex2rgb(color)
        h, s, v, k = RGBtoHSBK(rgb)
        new_zones.append((h, s, dim_level, k))
    try:
        strip.set_zone_colors(new_zones, duration, False)
    except WorkflowException as err:
        if count < retry_count:
            sleep(0.5 * (count + 1))
            set_colors(light_id, colors, dim_value=dim_value, count=count+1)
        else:
            logger.error("set_colors: Caught exception %s" % err)


def dim(light_id, dim_level, count=0):
    try:
        strip = get_or_create_light(light_id)
        all_zones = strip.get_color_zones()
        dim_zones = []
        dim_level = get_dim_value(dim_level)
        for [h, s, v, k] in all_zones:
            dim_zones.append((h, s, dim_level, k))
        strip.set_zone_colors(dim_zones, 3000, False)
    except WorkflowException as err:
        if count < retry_count:
            sleep(0.5 * (count + 1))
            dim(light_id, dim_level, count=count+1)
        else:
            logger.error("dim: Caught exception %s" % err)


def hex2rgb(hex):
    if hex[0] == "#":
        hex = hex.split("#")[1]
    red, green, blue = bytes.fromhex(hex)
    return red, green, blue


def get_dim_value(dim_value):
    dim_value = int(65535 * (int(dim_value) / 100))
    dim_value = 1000 if dim_value < 1000 else dim_value
    return dim_value
