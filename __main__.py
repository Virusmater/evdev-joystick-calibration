import evdev
from evdev import InputDevice, categorize, ecodes, AbsInfo


class MinMaxItem:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def __str__(self):
        return "minimum:" + str(self.minimum) + ";maximum:" + str(self.maximum)


devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if device.name == "Nintendo Wii Remote Classic Controller":
        device_path = device.path
min_max = {}
dev = InputDevice(device_path)

for event in dev.read_loop():
    if event.type == ecodes.EV_ABS:
        if event.code not in min_max:
            min_max[event.code] = MinMaxItem(event.value, event.value)
        if min_max[event.code].minimum > event.value:
            min_max[event.code].minimum = event.value
        if min_max[event.code].maximum < event.value:
            min_max[event.code].maximum = event.value
    if event.type == ecodes.EV_KEY:
        break


for code in min_max:
    dev.set_absinfo(code,  min=min_max[code].minimum, max=min_max[code].maximum)

dev.close()


