import argparse

import evdev
from evdev import ecodes

from evdev_joystick_calibration import configuration
from evdev_joystick_calibration.MinMaxItem import MinMaxItem


def main():
    parser = argparse.ArgumentParser(description='Pick up the gamepad and turn sticks with triggers around')
    parser.add_argument('-l', '--load', action='store_true', help='load configuration')
    parser.add_argument('-c', '--calibrate', action='store_true', help='calibrate and save configuration')
    args = parser.parse_args()
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    # If only load configuration - load available and exit
    if args.load:
        for index, device in enumerate(devices):
            if ecodes.EV_ABS in device.capabilities():
                try:
                    configuration.apply(device, configuration.load(device.name))
                except FileNotFoundError:
                    print("Skip", device.name)
                finally:
                    device.close()
        exit()

    # get all devices with analogs
    print('Available devices:')
    for index, device in enumerate(devices):
        if ecodes.EV_ABS in device.capabilities():
            print(index, device.name)
    print('Pick one device for the calibration:', end=" ")
    index = int(input())
    print('Move sticks and triggers of', devices[index].name, 'to max and min positions.')
    print('Press any button to apply.')

    min_max = {}
    device = devices[index]
    try:
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
    except KeyboardInterrupt:
        print('\rSave and apply the configuration? (y/n)', end=" ")
        answer = str(input())
        if answer == "y":
            pass
        else:
            exit()

    configuration.apply(device, min_max)
    configuration.store(device.name, min_max)
    device.close()


if __name__ == '__main__':
    main()
