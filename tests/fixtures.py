import os
import pytest
from config import config
from lifxlan import MultiZoneLight


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


@pytest.fixture(scope='function')
def setup_light_store():
    lightstore_dir = os.path.join(config.DIR, 'tests/lightstore')
    if not os.path.exists(lightstore_dir):
        os.mkdir(lightstore_dir)
    return lightstore_dir


@pytest.fixture
def light_store(setup_light_store):
    return os.path.join(config.DIR, 'tests/lightstore')
