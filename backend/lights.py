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

light_store = os.path.join(config.DIR, 'backend/lightstore')

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
    logger.info("Setting up light store")
    if not os.path.exists(light_store):
        os.mkdir(light_store)


def clear_light_store():
    if os.path.exists(light_store):
        logger.info("Removing and creating light store dir")
        shutil.rmtree(light_store)
    setup_light_store()


def get_power(label):
    light_obj = get_or_create_light(label)
    return light_obj.get_power()


def toggle_power(label):
    light_obj = get_or_create_light(label)
    power = light_obj.get_power()
    logger.info("turning light on")
    if not power:
        light_obj.set_power(True)
    else:
        light_obj.set_power(False)
    return light_obj.get_power()


def store_light(label, light_obj, lightdir=config.LIGHT_STORE_DIR):
    """
    If light is a multizone light (like a light strip or beam), append "_multizone_"
    to the label. This will be used by the frontend to show a different UI that allows
    multiple color choices
    """
    if isinstance(light_obj, MultiZoneLight):
        if "_multizone_" not in label:
            label = "_multizone_%s" % label
    light_path = os.path.join(lightdir, label)

    with open(light_path, "wb") as f:
        pickle.dump(light_obj, f)
    return light_obj


def get_stored_lights():
    all_stored_lights = []
    all_labels = os.listdir(light_store)
    for label in all_labels:
        light_path = os.path.join(light_store, label)
        with open(light_path, "rb") as f:
            light_obj = pickle.load(f)
            all_stored_lights.append((label, light_obj.get_mac_addr()))
    return all_stored_lights


def get_or_create_light(label, mac_address=None):
    if not label:
        raise Exception("No light found", label)
    print("getting light with label", label)
    light_path = os.path.join(light_store, label)
    if os.path.exists(light_path):
        with open(light_path, "rb") as f:
            light_obj = pickle.load(f)
            light_obj.set_label(label)
    else:
        logger.info("Creating light %s" % label)
        light_obj = get_light(mac_address)
        # if light is type MultiZoneLight, add (Z) in label
        # if type(light_obj) == multizonelight.MultiZoneLight:
        #     label_parts = label.split("_")
        #     label_parts[0] = label_parts[0] + "_" + "(Z)"
        #     label = "_".join(label_parts)
        light_obj.set_label(label)
        # turn light on
        store_light(label, light_obj)

    # if we're using real lights, really turn them on:
    # if not config.USE_LIGHT_FIXTURES:
    #     turn_light_on(light_obj)
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
                set_color(label, color=None, dim_value=dim_value)
        else:
            # bulb = get_or_create_light(label)
            # if "(Z)"
            set_color(label, color=None, dim_value=dim_value)
            # all_zones = strip.get_color_zones()
            # dim_zones = []
            # for [h, s, v, k] in all_zones:
            #     dim_zones.append((h, s, dim_value, k))
            # strip.set_zone_colors(dim_zones, 3000, False)
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
