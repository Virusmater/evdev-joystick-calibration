import json
import os
from os.path import expanduser

from MinMaxItem import MinMaxItemEncoder, object_decoder

conf_path = expanduser("~") + "/.config/evdev-joystick-calibration"


def store(name, min_max):
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    conf_name = get_name(name)
    with open(conf_path + "/" + conf_name, 'w') as outfile:
        json.dump(min_max, outfile, cls=MinMaxItemEncoder)


def load(name):
    conf_name = get_name(name)
    with open(conf_path + "/" + conf_name, 'r') as outfile:
        min_max = json.load(outfile, object_hook=object_decoder)
        return min_max


def get_name(name):
    return name.replace(" ", "") + ".json"
