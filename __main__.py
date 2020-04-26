import evdev
from evdev import InputDevice, ecodes


class MinMaxItem:
    def __init__(self, analog, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
        self.analog = analog

    def __str__(self):
        return "analog: " + self.analog + " min:" + str(self.minimum) + " max:" + str(self.maximum)


# get all devices with analogs
print('Available devices:')
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for index, device in enumerate(devices):
    caps = device.capabilities()
    if ecodes.EV_ABS in device.capabilities():
        print(index, device.name)
        device_path = device.path
print('Pick one device for the calibration:', end=" ")
index = int(input())
print('Move sticks and triggers of', devices[index].name, 'to max and min positions.')
print('Press any button to apply.')
device_path = devices[index].path

min_max = {}
dev = InputDevice(device_path)

for event in dev.read_loop():
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

print("\rNew configuration:", "              ")
for code in min_max:
    print(min_max[code])
    dev.set_absinfo(code,  min=min_max[code].minimum, max=min_max[code].maximum)

dev.close()


