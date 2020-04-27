import json


class MinMaxItem:
    def __init__(self, analog, minimum, maximum):
        self.minimum = int(minimum)
        self.maximum = int(maximum)
        self.analog = analog

    def __str__(self):
        return "analog: " + self.analog + " min:" + str(self.minimum) + " max:" + str(self.maximum)


class MinMaxItemEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def object_decoder(obj):
    if 'analog' in obj:
        return MinMaxItem(obj['analog'], obj['minimum'], obj['maximum'])
    return obj
