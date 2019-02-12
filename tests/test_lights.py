import os
import pickle
import shutil

import pytest

from lifxlan import MultiZoneLight

from config import config
from backend import lights



@pytest.fixture(scope='function')
def get_lights():
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
def setup_light_store():
    lightstore_dir = os.path.join(config.DIR, 'tests/lightstore')
    if not os.path.exists(lightstore_dir):
        os.mkdir(lightstore_dir)
    return lightstore_dir


@pytest.fixture
def light_store(setup_light_store):
    return os.path.join(config.DIR, 'tests/lightstore')


def clean_up_light_store(light_store):
    shutil.rmtree(light_store)


def test_store_lights(get_lights, setup_light_store):
    light_store = setup_light_store
    lights_to_store = get_lights
    stored_lights = lights.store_lights(lights_to_store, lightdir=light_store)
    assert len(lights_to_store) == len(stored_lights)
    lightdir_contents = os.listdir(light_store)
    assert len(lightdir_contents) == len(lights_to_store)
    for light in lights_to_store:
        light_id = light.mac_addr.replace(":", "")
        light_path = os.path.join(light_store, light_id)
        with open(light_path, "rb") as f:
            light_obj = pickle.load(f)
            assert isinstance(light_obj, MultiZoneLight)

    clean_up_light_store(light_store)

