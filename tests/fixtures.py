import os
import shutil
import pytest
from config import config_test as config

from lifxlan import Light, MultiZoneLight


def lifx_lights():
    single_zone_lights = [
        {
            "mac_addr": "12:34:56:78:9a:bc",
            "ip_addr": "192.168.0.2"
        },
        {
            "mac_addr": "12:45:56:99:9a:bc",
            "ip_addr": "192.168.0.3"
        }
    ]

    multi_zone_lights = [
        {
            "mac_addr": "23:45:67:89:ab:cd",
            "ip_addr": "192.168.0.4"
        }
    ]

    light_objects = []
    for light in single_zone_lights:
        light_objects.append(Light(light["mac_addr"], light["ip_addr"]))

    for light in multi_zone_lights:
        light_objects.append(MultiZoneLight(light["mac_addr"], light["ip_addr"]))

    return light_objects


@pytest.fixture(scope='function')
def get_lights():
    return lifx_lights()


@pytest.fixture(scope='function')
def setup_light_store():
    lightstore_dir = config.LIGHT_STORE_DIR
    print("using lightstore", lightstore_dir)
    if not os.path.exists(lightstore_dir):
        os.mkdir(lightstore_dir)
        assert os.path.exists(lightstore_dir)
    return lightstore_dir


@pytest.fixture
def light_store(setup_light_store):
    return os.path.join(config.DIR, 'tests/lightstore')


@pytest.fixture(autouse=True)
def remove_light_store(light_store):
    yield
    shutil.rmtree(light_store)
