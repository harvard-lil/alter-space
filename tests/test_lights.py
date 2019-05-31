import os
import pickle
from unittest import mock

from lifxlan import LifxLAN, Light, MultiZoneLight
from backend import lights
from config import config

lan = LifxLAN()
m = mock.Mock()


def test_store_light(get_lights, setup_light_store):
    ls = setup_light_store
    # storing singlezone light
    table_lamp = get_lights[0]
    label = "Table Lamp"
    lights.store_light(label, table_lamp, lightdir=ls)
    lightdir_contents = os.listdir(ls)
    assert len(lightdir_contents) == 1

    light_path = os.path.join(ls, label)
    with open(light_path, "rb") as f:
        light_obj = pickle.load(f)
        assert isinstance(light_obj, Light)

    # storing multizone light
    light_strip = get_lights[2]
    label = "Light Strip"
    lights.store_light(label, light_strip, lightdir=ls)
    lightdir_contents = os.listdir(ls)
    assert len(lightdir_contents) == 2

    light_path = os.path.join(ls, "%s%s" % (config.MULTICOLOR_INDICATOR, label))
    with open(light_path, "rb") as f:
        light_obj = pickle.load(f)
        assert isinstance(light_obj, MultiZoneLight)


def test_get_stored_lights(get_lights, setup_light_store):
    all_lights = lights.get_stored_lights()
    assert len(all_lights) == 0
    ls = setup_light_store
    table_lamp = get_lights[0]
    label = "Table Lamp"
    lights.store_light(label, table_lamp, lightdir=ls)
    lightdir_contents = os.listdir(ls)
    assert len(lightdir_contents) == 1
    all_lights = lights.get_stored_lights()
    assert len(all_lights) == 1


# @mock.patch('lan.get_lights', return_value=get_lights)
def x_test_get_or_create_light(mocker):
    stub = mocker.stub(name='get_lights_stub')

    lan.get_lights(stub)
    # mocker.patch('lan.get_lights', get_lights)
    light_obj = lights.get_or_create_light("Standing Light", "12:34:56:78:9a:bc")
    print('getting light object:', light_obj)
    assert False
