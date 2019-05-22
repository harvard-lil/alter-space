import os
import pickle
import shutil
from unittest import mock

from tests.fixtures import *
from lifxlan import LifxLAN, MultiZoneLight
from backend import lights

lan = LifxLAN()
m = mock.Mock()


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


# @mock.patch('lan.get_lights', return_value=get_lights)
def x_test_get_or_create_light(mocker):
    stub = mocker.stub(name='get_lights_stub')

    lan.get_lights(stub)
    # mocker.patch('lan.get_lights', get_lights)
    light_obj = lights.get_or_create_light("Standing Light", "12:34:56:78:9a:bc")
    print('getting light object:', light_obj)
    assert False
