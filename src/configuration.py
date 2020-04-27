import json
import os
from os.path import expanduser

from src.MinMaxItem import MinMaxItemEncoder, object_decoder

conf_path = expanduser("~") + "/.config/evdev-joystick-calibration/"


def store(name, min_max):
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    conf_name = conf_path + __get_name(name)
    with open(conf_name, 'w') as outfile:
        json.dump(min_max, outfile, cls=MinMaxItemEncoder)
    print("Configuration for", name, "saved at", conf_name)


def load(name):
    conf_name = conf_path + __get_name(name)
    with open(conf_name, 'r') as outfile:
        min_max = json.load(outfile, object_hook=object_decoder)
        print("Configuration for", name, "loaded from", conf_name)
        return min_max


def apply(dev, conf):
    print("\rConfiguration for", dev.name)
    for conf_code in conf:
        print(conf[conf_code])
        dev.set_absinfo(int(conf_code), min=conf[conf_code].minimum, max=conf[conf_code].maximum)


def __get_name(name):
    return name.replace(" ", "") + ".json"
