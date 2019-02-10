from time import sleep
from random import randint

from lifxlan import LifxLAN
from lifxlan.utils import RGBtoHSBK
lan = LifxLAN()
lights = lan.get_lights()


def get_light(id):
    # if not len(lights):
    lights = lan.get_lights()
    while not len(lights):
        sleep(1)
        lights = lan.get_lights()
    mac_addr = ""
    for key, part in enumerate(id):
        if (key + 2) % 2 == 0 and key != 0:
            mac_addr += ":"
        mac_addr += part
    for light in lights:
        if mac_addr in light.device_characteristics_str(""):
            return light
    raise Exception("No light found at id %s" % id)


def breathe(id):
    strip = get_light(id)
    all_zones = strip.get_color_zones()
    original_zones = all_zones
    dim_zones = []
    bright_zones = []
    for [h, s, v, k] in all_zones:
        dim_zones.append((h, s, 20000, k))
        bright_zones.append((h, s, 55535, k))

    # print("therefore", low, high)
    strip.set_zone_colors(bright_zones, 2000, True)
    sleep(randint(2, 10))
    strip.set_zone_colors(dim_zones, 2000, True)
    sleep(randint(2, 10))


def set_colors(id, colors, dim_value):
    # TODO: transition nicely
    strip = get_light(id)
    new_zones = []
    dim_level = get_dim_value(dim_value)
    for idx, color in enumerate(colors):
        rgb = hex2rgb(color)
        h, s, v, k = RGBtoHSBK(rgb)
        new_zones.append((h, s, dim_level, k))
    strip.set_zone_colors(new_zones, 3000, False)


def dim(id, dim_level):
    strip = get_light(id)
    all_zones = strip.get_color_zones()
    dim_zones = []
    dim_level = get_dim_value(dim_level)
    for [h, s, v, k] in all_zones:
        dim_zones.append((h, s, dim_level, k))
    strip.set_zone_colors(dim_zones, 3000, False)


def hex2rgb(hex):
    if hex[0] == "#":
        hex = hex.split("#")[1]
    red, green, blue = bytes.fromhex(hex)
    return red, green, blue


def get_dim_value(dim_value):
    dim_value = int(65535 * (int(dim_value)/100))
    dim_value = 1000 if dim_value < 1000 else dim_value
    return dim_value

