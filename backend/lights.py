import os
import shutil
from time import sleep
import logging

import pickle

from lifxlan import LifxLAN, MultiZoneLight
from lifxlan.errors import WorkflowException
from lifxlan.utils import RGBtoHSBK

from tests import fixtures
from config import config

logger = logging.getLogger()

lan = LifxLAN()

retry_count = 5


def discover_lights():
    lights = lan.get_lights()
    count = 0
    while count < retry_count and len(lights) == 0:
        lights = lan.get_lights()
        count += 1
        sleep(0.5)
    return lights


def setup_light_store():
    # Clear store before setting lights again
    if not os.path.exists(config.LIGHT_STORE_DIR):
        logger.info("Setting up light store")
        os.mkdir(config.LIGHT_STORE_DIR)


def clear_light_store():
    if os.path.exists(config.LIGHT_STORE_DIR):
        logger.info("Removing and creating light store dir")
        shutil.rmtree(config.LIGHT_STORE_DIR)
    setup_light_store()


def get_power(label):
    light_obj = get_or_create_light(label)
    return light_obj.get_power()


def toggle_power(label, to_state=None):
    light_obj = get_or_create_light(label)
    power = light_obj.get_power()
    logger.info("turning light on")
    if to_state is not None:
        # if to_state is set, turn lights on or off accordingly
        light_obj.set_power(to_state)
    else:
        if not power:
            light_obj.set_power(True)
        else:
            light_obj.set_power(False)
    return light_obj.get_power()


def store_light(label, light_obj, lightdir=config.LIGHT_STORE_DIR):
    """
    If light is a multicolor light (like a light strip or beam), append config.MULTICOLOR_INDICATOR
    to the label. This will be used by the frontend to show a different UI that allows
    multiple color choices
    """
    if isinstance(light_obj, MultiZoneLight):
        if config.MULTICOLOR_INDICATOR not in label:
            label = "%s%s" % (config.MULTICOLOR_INDICATOR, label)
    light_path = os.path.join(lightdir, label)
    with open(light_path, "wb") as f:
        pickle.dump(light_obj, f)
    return light_obj


def get_stored_lights():
    all_stored_lights = []
    all_labels = os.listdir(config.LIGHT_STORE_DIR)
    for label in all_labels:
        light_path = os.path.join(config.LIGHT_STORE_DIR, label)
        with open(light_path, "rb") as f:
            light_obj = pickle.load(f)
            all_stored_lights.append((label, light_obj.get_mac_addr()))
    all_stored_lights.sort()
    return all_stored_lights


def get_or_create_light(label, mac_address=None):
    if not mac_address and not label:
        raise Exception("No light found. Both mac_address and label are missing.")
    if not label:
        label = mac_address
    light_path = os.path.join(config.LIGHT_STORE_DIR, label)
    if os.path.exists(light_path):
        with open(light_path, "rb") as f:
            light_obj = pickle.load(f)
            try:
                old_label = light_obj.get_label()
                if old_label != label:
                    light_obj.set_label(label)
            except WorkflowException:
                logger.info("failed getting label for %s" % label)
                pass
    else:
        logger.info("Creating light %s" % label)
        light_obj = get_light(mac_address)
        light_obj.set_label(label)
        store_light(label, light_obj)

    return light_obj


def get_light(mac_address, count=0):
    """
    Takes in a mac address and returns a lifxlan lights object.
    If `USE_LIGHT_FIXTURES` is on, it uses fixture lights defined in tests/fixtures.py
    """
    all_lights = []
    getting_lights_count = 0
    if config.USE_LIGHT_FIXTURES:
        all_lights = fixtures.lifx_lights()
        print(all_lights)
    else:
        while not (len(all_lights) and getting_lights_count < retry_count):
            logger.info("Getting all lights")
            all_lights = discover_lights()
            logger.info("All lights: %s" % all_lights)
            sleep(0.5 * getting_lights_count)
            getting_lights_count += 1

    # if mac address was entered without `:`, add them in
    if mac_address and ":" not in mac_address:
        mac_addr = ""
        for key, part in enumerate(mac_address):
            if (key + 2) % 2 == 0 and key != 0:
                mac_addr += ":"
            mac_addr += part
        mac_address = mac_addr
    for light in all_lights:
        if mac_address == light.get_mac_addr():
            logger.info("Light was found: %s" % mac_address)
            return light

    # wifi connection is bad? light wasn't found, try again
    if count < retry_count:
        logger.info("Light was not found. Retrying.")
        sleep(0.5 * (count + 1))
        get_light(mac_address, count=count + 1)
    else:
        logger.error("No light found at id %s" % mac_address)
        raise Exception("No light found at id %s" % mac_address)


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
            chase(light_id, count=count + 1)
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
            breathe(light_id, count=count + 1)
        else:
            logger.error("Breathe: Caught exception %s" % err)


def set_color(label, color=None, dim_value=100, count=0, duration=3000):
    logger.info("set_color called")
    light = get_or_create_light(label)
    dim_level = get_dim_value(dim_value)
    if not color:
        [h, s, v, k] = light.get_color()
    else:
        rgb = hex2rgb(color)
        h, s, v, k = RGBtoHSBK(rgb)
    light.set_color([h, s, dim_level, k], duration)


def set_colors(light_id, colors=None, dim_value=100, count=0, duration=500):
    strip = get_or_create_light(light_id)
    new_zones = []
    dim_level = get_dim_value(dim_value)
    using_existing_colors = False
    if not colors:
        colors = strip.get_color_zones()
        using_existing_colors = True

    for idx, color in enumerate(colors):
        # if not relying on existing colors, colors need to be converted
        if not using_existing_colors:
            rgb = hex2rgb(color)
            h, s, v, k = RGBtoHSBK(rgb)
        else:
            h, s, v, k = color
        new_zones.append((h, s, dim_level, k))
    try:
        strip.set_zone_colors(new_zones, duration, False)
    except WorkflowException as err:
        if count < retry_count:
            sleep(0.5 * (count + 1))
            set_colors(light_id, colors, dim_value=dim_value, count=count + 1)
        else:
            logger.error("set_colors: Caught exception %s" % err)


def dim(label, dim_value, count=0):
    """
    Set dim_value for light label
    If label is missing, set dim_value for all lights
    """
    try:
        if not label:
            lights = get_stored_lights()
            for (label, mac_addr) in lights:
                if config.MULTICOLOR_INDICATOR in label:
                    set_colors(label, colors=None, dim_value=dim_value)
                else:
                    set_color(label, color=None, dim_value=dim_value)
        else:
            if config.MULTICOLOR_INDICATOR in label:
                set_colors(label, colors=None, dim_value=dim_value)
            else:
                set_color(label, color=None, dim_value=dim_value)
    except WorkflowException as err:
        if count < retry_count:
            sleep(0.5 * (count + 1))
            dim(label, dim_value, count=count + 1)
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


def flicker(label, mac_addr):
    try:
        light = get_or_create_light(label, mac_addr)
        print("flicker: light found", label)
        if isinstance(light, MultiZoneLight):
            colors = light.get_color_zones()
            [h, s, v, k] = colors[0]
        else:
            [h, s, v, k] = light.get_color()
        light.set_color([h, s, 20000, k], 500)
        sleep(0.5)
        light.set_color([h, s, 55535, k], 500)
        sleep(0.5)
    except Exception as e:
        return "Exception caught %s" % e
