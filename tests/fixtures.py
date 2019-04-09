import pytest
from lifxlan import LifxLAN, MultiZoneLight


def lifx_lights():
    lights = [
        {
            "mac_addr": "12:34:56:78:9a:bc",
            "ip_addr": "192.168.0.2"
        },
        {
            "mac_addr": "12:45:56:99:9a:bc",
            "ip_addr": "192.168.0.3"
        }
    ]
    multizonelights = []
    for light in lights:
        multizonelights.append(MultiZoneLight(light["mac_addr"], light["ip_addr"]))

    return multizonelights


@pytest.fixture(scope='function')
def get_lights():
    return lifx_lights()
