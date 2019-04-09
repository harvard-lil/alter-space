import os
import pickle
import shutil

import pytest
from unittest import mock

from tests.fixtures import *
from lifxlan import LifxLAN, MultiZoneLight

from config import config
from backend import lights

lan = LifxLAN()
m = mock.Mock()


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


def test_store_light(get_lights, setup_light_store):
    light_store = setup_light_store
    table_lamp = get_lights[0]
    label = "Table Lamp"
    lights.store_light(label, table_lamp, lightdir=light_store)
    lightdir_contents = os.listdir(light_store)
    assert len(lightdir_contents) == 1

    light_path = os.path.join(light_store, label)
    with open(light_path, "rb") as f:
        light_obj = pickle.load(f)
        assert isinstance(light_obj, MultiZoneLight)

    clean_up_light_store(light_store)


