import argparse

import evdev
from evdev import ecodes

import configuration
from MinMaxItem import MinMaxItem


def apply(dev, conf):
    print("\rConfiguration for", device.name)
    for conf_code in conf:
        print(conf[conf_code])
        dev.set_absinfo(int(conf_code), min=conf[conf_code].minimum, max=conf[conf_code].maximum)


parser = argparse.ArgumentParser(description='Pick up the gamepad and turn sticks with triggers around')
parser.add_argument('-l', '--load', action='store_true', help='load configuration')
args = parser.parse_args()
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

# If only load configuration - load available and exit
if args.load:
    for index, device in enumerate(devices):
        caps = device.capabilities()
        if ecodes.EV_ABS in device.capabilities():
            try:
                apply(device, configuration.load(device.name))
            except FileNotFoundError:
                print("Skip", device.name)
            finally:
                device.close()
    exit()

# get all devices with analogs
print('Available devices:')
for index, device in enumerate(devices):
    caps = device.capabilities()
    if ecodes.EV_ABS in device.capabilities():
        print(index, device.name)
        device_path = device.path
print('Pick one device for the calibration:', end=" ")
index = int(input())
print('Move sticks and triggers of', devices[index].name, 'to max and min positions.')
print('Press any button to apply.')

min_max = {}
device = devices[index]

for event in device.read_loop():
    # exit if a regular key was pressed
    if event.type == ecodes.EV_KEY:
        break
    if event.type == ecodes.EV_ABS:
        if event.code not in min_max:
            analog_name = str(evdev.categorize(event)).partition(", ")[2]
            min_max[event.code] = MinMaxItem(analog_name, event.value, event.value)
        if min_max[event.code].minimum > event.value:
            min_max[event.code].minimum = event.value
        if min_max[event.code].maximum < event.value:
            min_max[event.code].maximum = event.value
        # best way I was able to get name of the analog
        analog_name = str(evdev.categorize(event)).partition(", ")[2]
        print("\r" + str(min_max[event.code]), "   ", end=" ")

apply(device, min_max)
configuration.store(device.name, min_max)
device.close()
