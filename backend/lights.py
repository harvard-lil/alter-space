from time import sleep

from lifxlan import LifxLAN
from lifxlan.utils import RGBtoHSBK
lan = LifxLAN()
# lights = lan.get_lights()


def get_light(id, lights=[]):
    if not len(lights):
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
        bright_zones.append((h, s, 65535, k))

    try:
        print("Breathing...")
        while True:
            strip.set_zone_colors(bright_zones, 2000, True)
            sleep(2)
            strip.set_zone_colors(dim_zones, 2000, True)
            sleep(2)
    except KeyboardInterrupt:
        strip.set_zone_colors(original_zones, 1000, True)


def set_colors(id, colors):
    # TODO: transition nicely
    strip = get_light(id)
    new_zones = []
    for idx, color in enumerate(colors):
        print("color:", color)
        rgb = hex2rgb(color)
        h, s, v, k = RGBtoHSBK(rgb)
        new_zones.append((h, s, v, k))
    strip.set_zone_colors(new_zones, 3000, False)


def hex2rgb(hex):
    print("getting hex", hex)
    if hex[0] == "#":
        hex = hex.split("#")[1]
    red, green, blue = bytes.fromhex(hex)
    return red, green, blue
